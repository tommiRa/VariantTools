import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
import numpy as np

'''
Set color for domains if there are more than 7 distinct domains cycle colors.
More colors should be added!
'''
def setColor(i):
    return(["blue", "green", "red", "cyan", "magenta", "yellow", "purple"][i % 7])

def parse_domain_json(inputdom):
  '''
  Function parses domain input input file (json format) obtained from PFAM
  database. Function takes the json file as input and outputs the length of the 
  protein and a dictionary in which the keys are the domain descriptions and
  values are list of
  tuples of start and end positions of the domains
  '''
    # "P51587.json"
    f = open(inputdom)
    jdata = json.load(f)
    protein_dc = {"length":"", "domains":{}}
    protein_dc["length"] = int(jdata[u'length'])
    colorIndex = 0
    for i in range(0,len(jdata[u'regions'])):
        desc = str(jdata[u'regions'][i][u'metadata'][u'description'])
        print(desc)
        if desc not in protein_dc["domains"].keys():
            protein_dc["domains"][desc] = {}
            protein_dc["domains"][desc]["coordinates"] = []
            protein_dc["domains"][desc]["color"] = setColor(colorIndex)
            colorIndex += 1
        else:
            pass
        start = int(jdata[u'regions'][i][u'metadata'][u'aliStart'])
        end = int(jdata[u'regions'][i][u'metadata'][u'aliEnd'])
        protein_dc["domains"][desc]["coordinates"].append((start,end))
    return(protein_dc)

# Transform the coordinate (0,3000)
def transform(coord, length):
    return(3000*float(coord)/float(length))

#Plot the legend
def plotLegend(ax, protein_dc):

    # domain patches
    dom_patches = []
    for domain in protein_dc["domains"].keys():
        col = protein_dc["domains"][domain]["color"]
        dom_patches.append(patches.Patch(color = col, label = domain))

    plt.legend(handles = dom_patches , numpoints=1, loc=1, prop={'size':6})


    # Plot legends for variant types
    #line2 = mlines.Line2D(range(1), range(1), color="white",
    #markersize=15, marker='o',markerfacecolor="green")



def plotDomains(ax, fig1, protein_dc):

    # Extract protein length
    protein_length = protein_dc["length"]

    # Scale the thickness of the protein bbody based on the length of the
    # protein
    thickness_body = 100

    # Plot the protein body, the length is set to 3000
    ax.add_patch(
        patches.Rectangle((0,0), 3000, thickness_body, color = "grey")
    )

    # Plot the domains
    thickness_domain = 200

    # Plot the domains
    for domain_type in protein_dc['domains'].keys():
        for coordinates in protein_dc['domains'][domain_type]["coordinates"]:
            # Transform the coordinates to scale 0-3000
            print(coordinates)
            start = transform(coordinates[0], protein_length)
            end = transform(coordinates[1], protein_length)
            # Color
            col = protein_dc['domains'][domain_type]["color"]

            # Add domain to figure
            ax.add_patch(
                patches.Rectangle((start,-50), end - start, thickness_domain, color = col)
            )

    ax.set_ylim([-200, 1200])
    ax.set_xlim([-100, 3100])

    ticks_labs = np.arange(0,protein_length, 100).tolist()
    ticks_labs.append(protein_length)
    ticks_labs = np.array(ticks_labs)
    transformed_ticks = 3000*ticks_labs/protein_length
    ax.set_xticks(transformed_ticks)
    ax.set_xticklabels(ticks_labs)
    ax.set_yticks(np.arange(0,2400, 300))
    ax.set_yticklabels([0,1,2,3,4,5,6])

    # Plot the legend
    plotLegend(ax, protein_dc)

    fig1.savefig('test.pdf', format = "pdf", dpi=500, bbox_inches='tight')

def main():

    protein_dc = parse_domain_json("P51587.json")
    print(protein_dc)

    # Initialize Figure
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    plotDomains(ax1,fig1,protein_dc)

if __name__=="__main__":
    main()
