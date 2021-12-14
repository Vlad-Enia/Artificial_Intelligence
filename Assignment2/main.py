#1. Modelarea problemei ca o problemă de satisfacere a  constrângerilor
#  Problema colorării unei hărți

# Variabile: t1,t2,t3....,tn
# Domenii: c1,c2,....cm
# Constrangeri: Tarile vecine trebuie sa aiba culori diferite

# Construim un graf neorientat in care variabilele vor fi nodurile grafului.
# 2 tari sunt vecine daca au o muchie intre ele ( (ti,tj) - vecini <-> exista drum de la ti la tj de lungime 1 )
# Cerinta: p-colorare a grafului ( exista m partitii S1,S2,...,Sm  Si={tj1,tj2,tj3....,tjn} <-> any(i,j), i,j<m Si∩Sj={Ø} and S1US2U...USm={t1,t2,...,tn} and for each (tk1,tk2)⊆Si -> d(tk1,tk2)!=1


# def valid_coloring(country):
# #     for neighbour in country[1]:
# #         if all_countries[neighbour][2]==country[2]:
# #             return False
# #     return True


# Exemplul 1: considerăm o hartă cu regiunile WA, SA, NT; regiunile adiacente sunt precizate mai jos:
# WA: {SA, NT}
# SA: {WA, NT}
# NT: {WA, SA}
# Culorile disponibile pentru fiecare regiune sunt:
# WA: {red, green, blue}, SA: {red, green}, NT: {green}.
# WA=init('WA',['red','green','blue'],['SA','NT'])
# SA=init('SA',['red','green','blue'],['WA','NT','QS','NS','VT','TS'])
# NT=init('NT',['red','green','blue'],['WA','SA','QS'])
# QA=init('QA',['red','green','blue'])
#
# all_countries=dict()
# all_countries[WA[0]]=WA
# all_countries[SA[0]]=SA
# all_countries[NT[0]]=NT
#
# print(WA)
# print(SA)
# print(NT)
# print(all_countries)
#
# all_countries['WA'][3]='green'
# print(all_countries)
# print(valid_coloring(all_countries['WA']))
# all_countries['SA'][3]='green'
# print(all_countries)
# print(valid_coloring(all_countries['SA']))

#(0.5) 2. Implementarea metodei FC
#(0.2) 3. Implementarea MRV


import copy

def init(domain,neighbours):
    return [domain,neighbours,'']

all_countries=dict()
def load_countries():
    # you can instantiate a problem by giving a text file with the following structure:
    # the first row is the name of the country
    # the second row are the colours that a country can take
    # the third row are the neighbours of a country
    # repeat this structure for each country
    with open('instance') as file:
        counter=0
        name=None
        domain=None
        neighbours=None
        for line in file:
            if counter%3==0:
                name=line.rstrip()
            elif counter%3==1:
                domain=line.rstrip().split(',')
                if domain==['']:
                    domain=[]
            else:
                neighbours=line.rstrip().split(',')
                if neighbours==['']:
                    neighbours=[]
                all_countries[name]=init(domain,neighbours)
            counter+=1

load_countries()
print("Initial representation:\n",all_countries)

def get_key_with_minimum_domain(d):
    #returns the key of a country that doesn't have a colour assigned AND the domain of colors is minimum
    # (the uncoloured country with the least amount of colours available)
    key_names=list(d.keys())
    min_key=''
    for k in key_names:
        key_names.remove(k)
        if d[k][2]=='':
            min_key=k
            break
    for k in key_names:
        if d[k][2]=='':
            if len(d[k][0])<len(d[min_key][0]):
                min_key=k
    return min_key

def update_neighbours(d,key):
    # removes from the domain of the neighbours the colour assigned to the current element
    updated_element=d[key]
    neighbours=updated_element[1]
    for neighbour in neighbours:
        if updated_element[2] in d[neighbour][0]: d[neighbour][0].remove(updated_element[2])
    return d

def valid_coloring(d,key):
    # the coloring is valid if the domain of the neighbours is not empty (I can still assign a colour to all neighbours of the modified current country)
    updated_element=d[key]
    neighbours=updated_element[1]
    for neighbour in neighbours:
        if len(d[neighbour][0])==0 and d[neighbour][2]=='':
            return False
    return True

def get_uncolored_number(d):
    counter=0
    for k in d:
        if d[k][2]=='':
            counter+=1
    return counter

def forward_checking(d):
    key = get_key_with_minimum_domain(d)
    if key=='':
        print("Solution found!\n",d,"\n")
        return d
    possible_colors=d[key][0] # all possible colorings for the chosen uncoloured
    for color in possible_colors: #try to assign a colour from the domain
        new_d=copy.deepcopy(d)
        new_d[key][2]=color
        new_d=copy.deepcopy(update_neighbours(new_d,key))
        if valid_coloring(new_d,key):
            forward_checking(new_d) # if the coloring is valid we assign another country

forward_checking(all_countries)


