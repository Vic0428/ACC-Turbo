package ch.ethz.systems.netbench.xpt.ports.Pushback;

public class Cluster {
    public int prefix;
    public int bits;
    public int count;

    public Cluster (int count, int prefix) {
            this.prefix = prefix;
            this.count = count;
    }
}
