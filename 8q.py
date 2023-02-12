import numpy as np
import random as random
import math as math

popsize=10
generation=100

#init pop------------------------------
def init_pop():
    pop=np.zeros((popsize,8))
    for i in range(popsize):
        pop[i]=np.random.permutation([1,2,3,4,5,6,7,8])
    return pop
#------------------------------------------

#----------------------------------------
#-----------------------
def printchess(chrom):
    print('---------------------------------')
    for i in range(8):
        print('|',end='')
        for j in range(8):
            if 1+j==chrom[i]:
                print(' Q |',end='')
            else:
                print("   |",end='')
        print()
        print('---------------------------------')
#-------------------------------------------
def finess(chrom):
    sum=0
    for index in range(len(chrom)):
        chrom=list(chrom)
        col=index
        row=chrom[index]
        threat=0
        for i in range(len(chrom)):
            if i==col:
                continue
            if chrom[i]<row and chrom[i] + math.fabs(col-i)==row:
                threat=threat+1
            elif chrom[i]>row and chrom[i]-math.fabs(col-i)==row:
                threat=threat+1
        sum=sum+threat
    return sum
        
##----------------------------------
def selection(pop):
    murate=0.1
    crossrate=.3
    listedpop=[]
    for i in range(len(pop)):
        listedpop.append(list(pop[i]))
    pop=listedpop
    mupop_size=int(np.ceil(murate*popsize))
    crospop_size=(2*np.ceil(crossrate*popsize))
    childpop_size=mupop_size+crospop_size
    pop.sort(key=finess)
    chosen=pop[0:int(childpop_size)]
    return chosen

#----------------
def cross_over(p1, p2):#PMX
    r=random.sample(range(1,8),2)
    r.sort()
    r1,r2=r[0],r[1]
    p2=list(p2)
    p1=list(p1)

     
    middle1=p1[r1:r2]
    middle2=p2[r1:r2]

    child1=np.concatenate(((r1)*[0], middle1 ,(len(p1)-r2)*[0]),axis=0)
    child2=np.concatenate(((r1)*[0],middle2 ,(len(p2)-r2)*[0]),axis=0)

    for i in range(len(middle1)):
        if middle2[i] not in middle1:
            temp1=middle1[i]
            temp2=middle2[i]
            index=p2.index(temp1)
            while(p1[index] in middle1):
                temp1=p1[index]
                temp2=p2[index]
                index=p2.index(temp1)
            child1[index]=middle2[i]
    for i in range(len(child1)):
        if child1[i]==0:
             child1[i]=p2[i]
    for i in range(len(middle2)):
        if middle1[i] not in middle2:
            temp2=middle2[i]
            temp1=middle1[i]
            index=p1.index(temp2)
            while(p2[index] in middle2):
                temp2=p2[index]
                temp1=p1[index]
                index=p1.index(temp2)
            child2[index]=middle1[i]
    for i in range(len(child2)):
        if child2[i]==0:
             child2[i]=p1[i]
    return [child1,child2]
##----------------------------------------
def mutation(childs): #swap
    muindex=(random.sample(range(0,len(childs)),1))#choose child
    chrom=childs[muindex[0]]
    position1 = random.randint(0, len(chrom)-1)
    position2 = random.randint(0, len(chrom)-1)
    ########################chrom = list(chrom)
    temp = chrom[position1]
    chrom[position1] = chrom[position2]
    chrom[position2] = temp
    ############################################chrom = list(chrom)
    childs[muindex[0]]=chrom
    return childs
#-------------------------
def  survival_selection(population, childs):
    population=list(population)
    population.sort(key=finess)
    childs.sort(key=finess)
    population[-1] = childs[0]
    population[-2] = childs[1]
    population[-3] = childs[2]
    population[-4] = childs[3]
    
    
    fit=[]
    for i in range(len(population)):
        fit.append(finess(pop[i]))
    return population,fit
#genetic main loop-----------------------------
pop=init_pop()
mainpopsize=popsize
crossrate=.5
crospop_size=(2*np.ceil(crossrate*popsize)/2)
for iteration in range(generation):
    childs=[]
    print('generation',iteration)
    selected = selection(pop)  
    for i in range(0,int(crospop_size),2):    
        child1,child2=(cross_over(selected[i],selected[i+1]))
        childs.append(list(child1))
        childs.append(list(child2))
    childs = mutation(childs)
    newpop , bestfitness = survival_selection(pop, childs)
    pop=newpop
    print('best fitness:',bestfitness[0])
    if bestfitness[0]==0:
        printchess(pop[0])
        break
print('best soulution',newpop[0])
