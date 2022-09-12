
def prob_calculator(infection_rate=0.02,lc_chance=0.1, lc_healrate_short=0.65,lc_healrate_long=0.15,lc_stack_incr=0.01,lc_stack_max=0.5,lc_healrate_decay=0.01,lc_healrate_min=0.3,death_rate=0.001,death_rate_lc=0.005,years=30):
    '''
    infection_rate: weekly infection rate
    lc_chance : chance of initial lc
    lc_healrate_short : chance of healing in first 3 months 
    lc_healrate_long : chance of healing per year after 3 months of infection
    lc_stack_incr: chance of lc increased every time reinfection.
    lc_stack_max: maximum lc chance.
    death_rate: healthy death rate for each infection
    death_rate_lc: death rate if you already have lc.
    years: years calculated
    '''
    import numpy as np
    max_infected=500
    import copy
    lc_heal_weekly_chance=1-np.exp(np.log(1-lc_healrate_long)/52)
    #print(lc_heal_weekly_chance)
    # short-term lc transform to long-term lc/healthy under avg=3 months. 
    lc_short_transform_weekly_chance=1/(12-1)
    probs_by_covid_times=[]
    for i in range(max_infected+1):
        dic={'times_covid':i, 'total_chance':0, 'lc_short_chance':0,'lc_long_chance':0, 'healthy_chance':0, 'death_chance':0}
        probs_by_covid_times.append(copy.deepcopy(dic))
        
    # week 0
    probs_by_covid_times[0]['total_chance']=1
    probs_by_covid_times[0]['healthy_chance']=1
    chart=[]
    #print(lc_stack_max)
    for i in range(1,52*years+1):
        # for every week, update current lc healing status

        for nums_infected in range(1,max_infected+1):
            # healing of long-term lc 
            short_healrate=max(lc_healrate_short-lc_healrate_decay*nums_infected,lc_healrate_min)
            probs_by_covid_times[nums_infected]['lc_long_chance']*=1-lc_heal_weekly_chance
            # transformation of short-term lc
            probs_by_covid_times[nums_infected]['lc_long_chance']+= lc_short_transform_weekly_chance*probs_by_covid_times[nums_infected]['lc_short_chance']*(1-short_healrate)
            probs_by_covid_times[nums_infected]['lc_short_chance']*=1-lc_short_transform_weekly_chance

            probs_by_covid_times[nums_infected]['healthy_chance']=probs_by_covid_times[nums_infected]['total_chance']-probs_by_covid_times[nums_infected]['lc_short_chance']-probs_by_covid_times[nums_infected]['lc_long_chance']-probs_by_covid_times[nums_infected]['death_chance']

        # new infections
        for nums_infected in range(max_infected,0,-1):
            #print(nums_infected)
            chance_of_new_infection=(probs_by_covid_times[nums_infected-1]['total_chance']-probs_by_covid_times[nums_infected-1]['death_chance'])*infection_rate
            chance_of_new_lc=min(lc_stack_incr*(nums_infected-1)+lc_chance, lc_stack_max)
            
            lc_increased=probs_by_covid_times[nums_infected-1]['healthy_chance']*infection_rate*chance_of_new_lc
            died=infection_rate*(death_rate*probs_by_covid_times[nums_infected-1]['healthy_chance']+death_rate_lc*(probs_by_covid_times[nums_infected-1]['lc_short_chance']+probs_by_covid_times[nums_infected-1]['lc_long_chance']))
            # status transform
            probs_by_covid_times[nums_infected]['total_chance']+=chance_of_new_infection
            probs_by_covid_times[nums_infected-1]['total_chance']-=chance_of_new_infection
            probs_by_covid_times[nums_infected]['death_chance']+=died
            probs_by_covid_times[nums_infected]['lc_short_chance']+=lc_increased+probs_by_covid_times[nums_infected-1]['lc_short_chance']*infection_rate
            probs_by_covid_times[nums_infected-1]['lc_short_chance']*=1-infection_rate
            probs_by_covid_times[nums_infected]['lc_long_chance']+=probs_by_covid_times[nums_infected-1]['lc_long_chance']*infection_rate
            probs_by_covid_times[nums_infected-1]['lc_long_chance']*=1-infection_rate
            probs_by_covid_times[nums_infected]['healthy_chance']=probs_by_covid_times[nums_infected]['total_chance']-probs_by_covid_times[nums_infected]['lc_short_chance']-probs_by_covid_times[nums_infected]['lc_long_chance']-probs_by_covid_times[nums_infected]['death_chance']
            probs_by_covid_times[nums_infected-1]['healthy_chance']*=1-infection_rate
        
        if (i%52==0):
            total_lc_chance=0
            total_death_chance=0
            total_healthy_chance=0
            avg_infection=0
            for nums_infected in range(max_infected+1):
                total_lc_chance+=probs_by_covid_times[nums_infected]['lc_short_chance']+probs_by_covid_times[nums_infected]['lc_long_chance']
                total_death_chance+=probs_by_covid_times[nums_infected]['death_chance']
                total_healthy_chance+=probs_by_covid_times[nums_infected]['healthy_chance']
                avg_infection+=nums_infected*probs_by_covid_times[nums_infected]['total_chance']
            dic={'years':i/52, 'lc_chance':total_lc_chance,'death_chance':total_death_chance,'healthy_chance':total_healthy_chance,'average_infections':avg_infection}
            #cprint(dic)
            chart.append(dic)
    
    return chart


import argparse
import numpy as np
parser=argparse.ArgumentParser(description="args")
parser.add_argument("--mode",type=str,default="realistic",help="base mode params, optimistic(opt), realistic(real), pessimistic(pessi)")
parser.add_argument("--weekly-infection-rate",type=float,default=None,help="weekly infection rate")
parser.add_argument("--infection-lc-chance",type=float,default=None,help="long covid chance at 1st infection")
parser.add_argument("--healrate-s",type=float,default=None,help="long covid heal rate within 3 months")
parser.add_argument("--healrate-l",type=float,default=None,help="annualized heal rate for long covid more than 3 months")
parser.add_argument("--infection-lc-incr",type=float,default=None,help="long covid chance increment for each infection")
parser.add_argument("--infection-lc-max",type=float,default=None,help="max long covid chance for each infection")
parser.add_argument("--healrate-s-decay",type=float,default=None,help="long covid heal rate within 3 months decay for each infections")
parser.add_argument("--healrate-s-min",type=float,default=None,help="long covid heal rate within 3 months min")
parser.add_argument("--death-rate",type=float,default=None,help="death rate for each infection, if you don't have long covid")
parser.add_argument("--death-rate-lc",type=float,default=None,help="death rate for each infection, if you already have long covid")
parser.add_argument("--years",type=float,default=None,help="simulation years")
args=parser.parse_args()
# optimistic params
param_sets=[]
if args.mode in ["real","realistic"]:
    param_sets=[0.03,0.13,0.65,0.25,0.015,0.5,0.01,0.3,0.002,0.01,50]
if args.mode in ["opt","optimistic"]:
    param_sets=[0.015,0.06,0.8,0.5,0.005,0.25,0,0.5,0.001,0.005,50]
if args.mode in ["pess","pessimistic"]:
    param_sets=[0.045,0.2,0.5,0.1,0.04,0.75,0.02,0,0.004,0.025,50]
    print(len(param_sets))
if args.weekly_infection_rate is not None:
    param_sets[0]=args.weekly_infection_rate
if args.infection_lc_chance is not None:
    param_sets[1]=args.infection_lc_chance
if args.healrate_s is not None:
    param_sets[2]=args.healrate_s
if args.healrate_l is not None:
    param_sets[3]=args.healrate_l
if args.infection_lc_incr is not None:
    param_sets[4]=args.infection_lc_incr
if args.infection_lc_max is not None:
    param_sets[5]=args.infection_lc_max
if args.healrate_s_decay is not None:
    param_sets[6]=args.healrate_s_decay
if args.healrate_s_min is not None:
    param_sets[7]=args.healrate_s_min
if args.death_rate is not None:
    param_sets[8]=args.death_rate
if args.death_rate_lc is not None:
    param_sets[9]=args.death_rate_lc
if args.years is not None:
    param_sets[10]=args.years

chart=prob_calculator(param_sets[0],param_sets[1],param_sets[2],param_sets[3],
param_sets[4],param_sets[5],param_sets[6],param_sets[7],param_sets[8],param_sets[9],param_sets[10])

report_years=[1,2,3,5,7,10,20,30,50]
for i in chart:
    if i["years"] in report_years:
        print(i)
