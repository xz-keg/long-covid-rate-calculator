
def prob_calculator(infection_rate=0.02,lc_chance=0.2, lc_healrate_short=0.8,lc_healrate_long=0.5,lc_stack_incr=0.01,lc_stack_max=0.5,death_rate=0.001,death_rate_lc=0.005,years=30):
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
    lc_short_transform_weekly_chance=1/(13-1)
    probs_by_covid_times=[]
    for i in range(max_infected+1):
        dic={'times_covid':i, 'total_chance':0, 'lc_short_chance':0,'lc_long_chance':0, 'healthy_chance':0, 'death_chance':0}
        probs_by_covid_times.append(copy.deepcopy(dic))
        
    # week 0
    probs_by_covid_times[0]['total_chance']=1
    probs_by_covid_times[0]['healthy_chance']=1
    chart=[]
    for i in range(1,52*years+1):
        # for every week, update current lc healing status
        for nums_infected in range(1,max_infected+1):
            # healing of long-term lc 
            probs_by_covid_times[nums_infected]['lc_long_chance']*=1-lc_heal_weekly_chance
            # transformation of short-term lc
            probs_by_covid_times[nums_infected]['lc_long_chance']+= lc_short_transform_weekly_chance*probs_by_covid_times[nums_infected]['lc_short_chance']*(1-lc_healrate_short)
            probs_by_covid_times[nums_infected]['lc_short_chance']*=1-lc_short_transform_weekly_chance

            probs_by_covid_times[nums_infected]['healthy_chance']=probs_by_covid_times[nums_infected]['total_chance']-probs_by_covid_times[nums_infected]['lc_short_chance']-probs_by_covid_times[nums_infected]['lc_long_chance']-probs_by_covid_times[nums_infected]['death_chance']

        # new infections
        for nums_infected in range(max_infected,0,-1):
            #print(nums_infected)
            chance_of_new_infection=(probs_by_covid_times[nums_infected-1]['total_chance']-probs_by_covid_times[nums_infected-1]['death_chance'])*infection_rate
            chance_of_new_lc=max(lc_stack_incr*(nums_infected-1)+lc_chance, lc_stack_max)
            
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
            print(dic)
            chart.append(dic)
    return chart

prob_calculator()

