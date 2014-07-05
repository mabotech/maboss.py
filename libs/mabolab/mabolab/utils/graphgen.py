
from random import randint

class GraphGen:

    def __init__(self, nodes, links, filename, label = ''):
        self.nodes = nodes
        self.links = links
        self.label = label
        self.filename = filename

        self.colors = ['darkgreen','red','navy','green','yellow','blue','violet','darksalmon','black','orangered','cyan','darkorange','beige','yellowgreen','black']

    def edgegen(self):

        dot = ''
        for item in self.links:
            color = self.colors[randint(0,len(self.colors)-1)]

            if int(item[1])<0:
                dest = 'Stop'

            else:
                dest = "id%s"%(item[1])

            if item[0] == '0':
                src = 'Start'
            else:
                src = "id%s"%(item[0])

            dot = dot +  '''%s -- %s [label="%s", color="%s"];\n'''%(src, dest, item[2], color)
        return dot

    def nodegen(self):
        self.n = ''
        for item in self.nodes:
            self.n = self.n + """id%s[label="    %s - %s    "];\n""" %(item[0], item[1], item[2])


    def gen(self):

        self.nodegen()

        g = """
    graph G {
      rankdir = TB;
      fontsize=10;
      fontname="simsun.ttc";
      label="%s"
      node[style=filled,color=lightskyblue, fontsize=10, fontname="simsun.ttc" ,shape=box];
      Start[label="Start" color=green shape=diamond];
      Stop[label="Stop" color=red ,shape=ellipse];
      edge[arrowhead=normal,fontsize=10, fontname="simsun.ttc" ];
      %s
      """ %(self.label, self.n)
        dot = file(self.filename,'w')

        dot.write(g)

        dotstr = self.edgegen()
        dot.write(dotstr)
        dot.write("}\n")

if __name__ == '__main__':
    links = [('0', '100012069', ''), ('100012069', '100012070', ''), ('100012073', '100012075', ''), ('100012075', '100012076', 'No'), ('100012075', '100012079', 'Yes'), ('100012080', '100012081', 'true'), ('100012081', '100012082', ''), ('100012079', '100012083', ''), ('100012083', '100012084', ''), ('100012083', '-1', 'Cancel'), ('100012074', '100012077', ''), ('100012072', '100012074', 'OK'), ('100012072', '-1', 'Cancel'), ('100012072', '100012073', 'GetWO'), ('100012082', '100012072', ''), ('100012070', '100012071', ''), ('100012071', '100012072', ''), ('100012077', '100012080', '\xe5\x88\xa0\xe9\x99\xa4\xe4\xb8\xad\xe6\x96\x87'), ('100012080', '100012072', ''), ('100012084', '100012086', 'AddDeviatedPart'), ('100012084', '100012085', 'Regular'), ('100012086', '100012085', '\xe6\x98\xaf'), ('100012085', '100012072', ''), ('100012076', '100012078', '2'), ('100012076', '100012077', '\xe5\x88\xa0\xe9\x99\xa4\xe4\xb8\xad\xe6\x96\x87'), ('100012078', '100012087', ''), ('100012087', '100012088', 'Rescan'), ('100012087', '-2', 'Logout'), ('100012087', '100012087', ''), ('100012088', '100012077', ''), ('100012087', '100012077', 'WSOperation'), ('100012074', '100012078', '2')]
    gg = GraphGen(links,'f001.dot', 'sub assembly v1.0')
    gg.output()
