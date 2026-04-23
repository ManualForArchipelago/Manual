import json
GG_medals = {1:5,4:5,5:5,6:5,7:5,8:5,10:5,
               2:3,3:3,9:3,
             11:0}

SC_medals = {1:5,3:5,4:5,6:5,7:5,8:5,9:5,
             2:3,5:3,10:3,11:3,
             12:0}

DR_medals = {3:5,5:5,6:5,7:5,8:5,9:5,10:5,
             1:3,2:3,4:3,11:3,
             12:0}

VV_medals = {1:5,2:5,5:5,6:5,7:5,10:5,11:5,
             3:3,4:3,8:3,9:3,
             12:0}

abbreviation = {"Green Grounds": "GG", "Sandy Canyon": "SC", "Dedede Resort": "DR", "Volcano Valley" : "VV", "Necro Nebula" : "NN"}
mapping_GG = {1:"Tutorial",
              2:"Outer Ring",3:"Outer Ring",4:"Outer Ring",
              5:"Middle Ring",6:"Middle Ring",7:"Middle Ring",
              8:"Inner Ring",9:"Inner Ring",10:"Inner Ring",
              11:"Boss"}
mapping_SC = {1:"Outer Ring",2:"Outer Ring",3:"Outer Ring",4:"Outer Ring",
              5:"Middle Ring",6:"Middle Ring",7:"Middle Ring",8:"Middle Ring",
              9:"Inner Ring",10:"Inner Ring",11:"Inner Ring",
              12:"Boss"}
mapping_DR = {1:"Outer Ring",2:"Outer Ring",3:"Outer Ring",4:"Outer Ring",
              5:"Middle Ring",6:"Middle Ring",7:"Middle Ring",
              8:"Inner Ring",9:"Inner Ring",10:"Inner Ring",11:"Inner Ring",
              12:"Boss"}
mapping_VV = {1:"Outer Ring",2:"Outer Ring",3:"Outer Ring",
              4:"Middle Ring",5:"Middle Ring",6:"Middle Ring",7:"Middle Ring",
              8:"Inner Ring",9:"Inner Ring",10:"Inner Ring",11:"Inner Ring",
              12:"Boss"}
mapping_NN = {1:"Outer Ring", 2:"Outer Ring", 3:"Outer Ring", 4:"Outer Ring",
              5:"Boss"}
mappings = {"GG":mapping_GG, "SC":mapping_SC, "DR":mapping_DR,"VV":mapping_VV, "NN":mapping_NN}
mappings_medal = {"GG":GG_medals, "SC":SC_medals, "DR":DR_medals,"VV":VV_medals}


def requirements_completion(stage_number, world_name, medal_number=0):
    requirements = ""
    if world_name == "Green Grounds":
        if stage_number == 1:
            requirements += "|Bubble Ability| and |Bomb Block|"
            if medal_number == 3:
                requirements += " and |Extra Kirby:5|"
            if medal_number == 0 or medal_number == 5:
                requirements += " and |Cannon|"
        if stage_number == 2:
            requirements += "|Melody Switch|"
            if medal_number ==3:
                requirements += " and |Keys|"
        if stage_number == 3:
            requirements += "|Cannon|"
            if medal_number ==2:
                requirements += " and |Extra Kirby:10|"
        if stage_number == 4:
            if medal_number == 1:
                requirements += "|Keys|"
            if medal_number == 2:
                requirements += "|Bubble Ability|"
            if medal_number == 4:
                requirements += "|Cannon| and |Extra Kirby:10|"
            if medal_number == 0:
                requirements += "!Cannon!"

    if world_name == "Sandy Canyon":
        if stage_number == 1:
            requirements += "|Bomb Block|"
        if stage_number == 2:
            if medal_number ==2:
                requirements += "|Extra Kirby:10|"
            if medal_number ==3:
                requirements += "|Cannon|"
        if stage_number == 3:
            requirements += "|Melody Switch|"
            if medal_number == 2:
                requirements += " and |Destroyable Brown Block|"
            if medal_number == 3:
                requirements += " and |Cannon|"
            if medal_number == 4 :
                requirements += " and |Extra Kirby:10|"
            if medal_number == 5 :
                requirements += " and |Bomb block| and |Skull Keys|"
        if stage_number == 4:
            if medal_number >= 3 :
                requirements += "|Cannon|"
            if medal_number == 3:
                requirements += " and |Extra Kirby:10|"
            if medal_number == 4:
                requirements += " and |Destroyable Brown Block| and |Keys|"
            if medal_number == 2:
                requirements += "|Bomb Block|"
            if medal_number == 0:
                requirements += "(|Bomb Block| and |Melody Switch|) or |Cannon|"
        if stage_number == 5:
            requirements += "|Bomb Block|"
            if medal_number == 1:
                requirements += " and |Keys|"
        if stage_number == 6:
            requirements += "|Destroyable Brown Block|"
            if medal_number >=3 or medal_number == 0:
                requirements+= " and |Normal Switch|"
            if medal_number >= 4 :
                requirements += " and |Extra Kirby:10|"
        if stage_number == 7:
            if medal_number == 1:
                requirements += "|Extra Kirby:10|"
            if medal_number == 2:
                requirements += "|Jumbo Candy|"
            if medal_number == 3:
                requirements += "|Skull Keys|"
            if medal_number == 4 or medal_number == 5 or medal_number == 0:
                requirements+= "|Melody Switch| and |Destroyable Brown Block|"
            if medal_number == 5:
                requirements += " and |Keys| and |Extra Kirby:10|"



    return requirements

import pandas as pd
doc = pd.read_excel("Kirby Mass Attack Requirements.ods",0)
doc1 = pd.DataFrame(pd.read_excel("Kirby Mass Attack Requirements.ods",1))
print(doc1)
print(type(doc1))
doc1["World"] = doc1["World"].ffill()
print(doc1)
doc1["Stage"] = doc1["Stage"].ffill()
print(doc1)
doc1.fillna(0, inplace=True)

def template_completion(stage_number, world_name, doc):
    return {"name": f"Stage {stage_number} ({abbreviation[world_name]}) completed",
                      "region": f"{world_name} - {mappings[abbreviation[world_name]][stage_number]}",
                      "category": ["Stage Completion", world_name],
                      "requires": f"|Kirby:{doc.loc[(doc['World'] == world_name) & (doc['Stage'] == stage_number)].iloc[0]["Kirbys"]}|"}

def template_medal(medal_number, stage_number, world_name, doc, doc1):
    requirements = f"|Kirby:{doc.loc[(doc['World'] == world_name) & (doc['Stage'] == stage_number)].iloc[0]["Kirbys"]}|"
    row = doc1.loc[(doc1['World'] == world_name) & (doc1['Stage'] == stage_number) & (doc1['Medal'] == medal_number)]
    print(row)
    if row.iloc[0]["Kirbys"]:
        requirements += f" and |Kirby:{int(row.iloc[0]["Kirbys"])}|"
    if row.iloc[0]["Keys"]:
        requirements += f" and |Keys:1|"
    if row.iloc[0]["Skull Keys"]:
        requirements += f" and |Skull Keys:1|"
    if row.iloc[0]["Jumbo Candy"]:
        requirements += f" and |Jumbo Candy:1|"

    return {"name": f"Stage {stage_number} - Medal {medal_number} ({abbreviation[world_name]})",
                      "region": f"{world_name} - {mappings[abbreviation[world_name]][stage_number]}",
                      "category": ["Medal", world_name],
                      "requires": requirements}

def add_medal_locations(loc, stage_number, world_name, doc, doc1):
    for n in range(1, mappings_medal[abbreviation[world_name]][stage_number]+1):
        loc.append(template_medal(n, stage_number,world_name, doc, doc1))

locations =  []
for i in range(1, 12):
    locations.append(template_completion(i, "Green Grounds", doc))
    add_medal_locations(locations,i,"Green Grounds", doc, doc1)

for i in range(1, 13):
    locations.append(template_completion(i, "Sandy Canyon", doc))
    locations.append(template_completion(i, "Dedede Resort", doc))
    locations.append(template_completion(i, "Volcano Valley", doc))
    add_medal_locations(locations, i, "Dedede Resort", doc, doc1)
    add_medal_locations(locations, i, "Sandy Canyon", doc, doc1)
    add_medal_locations(locations, i, "Volcano Valley", doc, doc1)

for i in range(1, 6):
    locations.append(template_completion(i, "Necro Nebula", doc ))
locations[-1]["victory"] = True
locations[-1]["category"] = ["Necro Nebula"]


with open("worlds/manual_kirbymassattack_simularbre/data/locations.json", "w") as f:
    json.dump(locations, f,indent=4)
