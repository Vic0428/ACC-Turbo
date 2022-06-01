--- On one queue: Replay a pcap file
--- On the other queues: Generate a DDoS attack on top

local mg      = require "moongen"
local device  = require "device"
local memory  = require "memory"
local stats   = require "stats"
local log     = require "log"
local pcap    = require "pcap"
local limiter = require "software-ratecontrol"
local timer  = require "timer"

function configure(parser)
        -- general configs
        parser:argument("dev", "Device to use."):default(3):convert(tonumber)

        -- configs for the pcap generation
        parser:argument("file", "File to replay."):args(1)
        parser:option("-pr --pcap-rate-multiplier", "Speed up or slow down replay, 1 = use intervals from file, default = replay as fast as possible"):default(0):convert(tonumber):target("rateMultiplier")
        parser:flag("-l --loop", "Repeat pcap file.")

        local args = parser:parse()
        return args
end

function master(args)
        -- we set 4 queues to the interface
        local dev = device.config{port = args.dev, txQueues = 4}
	device.waitForLinks()

        -- replay pcap using the first queue
        local rateLimiter
        if args.rateMultiplier > 0 then
                rateLimiter = limiter:new(dev:getTxQueue(0), "custom")
        end
        mg.startTask("replay_pcap", dev:getTxQueue(0), args.file, args.loop, rateLimiter, args.rateMultiplier)
        stats.startStatsTask{txDevices = {dev}}

        -- ATTACK GENERATION
        local flows = 1
        local packetSize = 1200
        local attackID = 1

        mg.sleepMillis(10000)
        mg.startTask("launch_attack", dev:getTxQueue(1), packetSize, flows, 1)
        mg.startTask("launch_attack", dev:getTxQueue(2), packetSize, flows, 1)
        mg.startTask("launch_attack", dev:getTxQueue(3), packetSize, flows, 1)
        mg.sleepMillis(20000)
        mg.startTask("launch_attack", dev:getTxQueue(1), packetSize, flows, 2)
        mg.startTask("launch_attack", dev:getTxQueue(2), packetSize, flows, 2)
        mg.startTask("launch_attack", dev:getTxQueue(3), packetSize, flows, 2)
        mg.sleepMillis(20000)
        mg.startTask("launch_attack", dev:getTxQueue(1), packetSize, flows, 3)
        mg.startTask("launch_attack", dev:getTxQueue(2), packetSize, flows, 3)
        mg.startTask("launch_attack", dev:getTxQueue(3), packetSize, flows, 3)
        mg.sleepMillis(20000)
        mg.startTask("launch_attack", dev:getTxQueue(1), packetSize, flows, 4)
        mg.startTask("launch_attack", dev:getTxQueue(2), packetSize, flows, 4)
        mg.startTask("launch_attack", dev:getTxQueue(3), packetSize, flows, 4)
        mg.sleepMillis(20000)
        
        -- monitor progress
        mg.stop()
        mg.waitForTasks()
end

function launch_attack(queue, size, flows, id)

        -- attack packet configuration
        local DST_MAC           = "3c:fd:fe:b4:98:91" -- resolved via ARP on GW_IP or DST_IP, can be overriden with a string here
        local SRC_IP            = "10.0.0.50"
        local DST_IP            = "20.0.0.50"
        local SRC_PORT          = 111
        local DST_PORT          = 222
        
        local mempool = memory.createMemPool(function(buf)

                local DST_IP_MOD = nil
                if id == 1 then
                        DST_IP_MOD = parseIPAddress("20.0.0.50")
                elseif id == 2 then
                        DST_IP_MOD = parseIPAddress("20.0.0.100")
                elseif id == 3 then
                        DST_IP_MOD = parseIPAddress("20.0.0.150")
                elseif id == 4 then
                        DST_IP_MOD = parseIPAddress("20.0.0.200")
                end

                buf:getUdpPacket():fill{ 
                        ethSrc = queue, -- get the src mac from the device
                        ethDst = DST_MAC,
                        ip4Src = SRC_IP,
                        ip4Dst = DST_IP_MOD,
                        ip4TOS = 0,
                        ipv4Length = 0,
                        ip4TTL = 250,
                        -- ipProtocol
                        ip4ID  = 0,
                        udpSrc = SRC_PORT,
                        udpDst = DST_PORT,
                        pktLength = size -- this sets all length headers fields in all used protocols
                        -- udpLength
                        -- udpChecksum 
                        -- payload will be initialized to 0x00 as new memory pools are initially empty
                }
        end)

        local bufs = mempool:bufArray() -- a buf array is essentially a very thing wrapper around a rte_mbuf*[], i.e. an array of pointers to packet buffers
        RUN_TIME = 10 -- seconds
	local runtime = timer:new(RUN_TIME)
        while mg.running() and runtime:running() do -- check if Ctrl+c was pressed
        	-- this actually allocates some buffers from the mempool the array is associated with
		-- this has to be repeated for each send because sending is asynchronous, we cannot reuse the old buffers here
                bufs:alloc(size)

                -- UDP checksums are optional, so using just IPv4 checksums would be sufficient here
                -- UDP checksum offloading is comparatively slow: NICs typically do not support calculating the pseudo-header checksum so this is done in SW
                bufs:offloadUdpChecksums()
                -- send out all packets and frees old bufs that have been sent
                queue:send(bufs)

                -- Rate limiting
                --mg.sleepMicros(58) -- tunned such that each attack sends at 10Gbps with framing
        end
end

function replay_pcap(queue, file, loop, rateLimiter, multiplier)
        local mempool = memory:createMemPool(4096)
        local bufs = mempool:bufArray()
        local pcapFile = pcap:newReader(file)
        local prev = 0
        local linkSpeed = queue.dev:getLinkStatus().speed -- important, this used to be queue.dev:getLinkStatus().speed, but the speed there is wrong

	while mg.running() do
		local n = pcapFile:read(bufs)
		if n > 0 then
			if rateLimiter ~= nil then
				if prev == 0 then
					prev = bufs.array[0].udata64
				end
				for i = 1, n  do
					local buf = bufs[i]
					-- ts is in microseconds
					local ts = buf.udata64
					if prev > ts then
						ts = prev
					end
					local delay = ts - prev
					delay = tonumber(delay * 10^3) / multiplier -- nanoseconds
					delay = delay / (8000 / linkSpeed) -- delay in bytes
					buf:setDelay(delay)
					prev = ts
				end
			end
		else
			if loop then
				pcapFile:reset()
			else
				break
			end
		end
		if rateLimiter then
			rateLimiter:sendN(bufs, n)
		else
			queue:sendN(bufs, n)
		end
	end
        log:info("Flushing buffers, this can take a while...")
end