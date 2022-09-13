# long-covid-rate-calculator

calculate the probability of you getting long covid after "living with virus" for years. 

Parameters:

``weekly-infection-rate``: The rate of you getting a new infection in any week. According to ONS data, this number averaged to be around 3% in UK in 2022. 
Source: https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/bulletins/coronaviruscovid19infectionsurveypilot/2september2022    

``infection-lc-chance``: The UK’s National Institute for Health Care and Excellence (NICE) defines COVID-19 symptom duration with three categories: <4 weeks, 4–12 weeks, and >12 weeks),with the latter two categories both considered ‘long COVID’. The rate of you getting long covid() after each infection. 

Source: https://www.nature.com/articles/s41467-022-30836-0

``healrate-s``: short term heal rate for long covid. The proportion of 4-12 week LC transformed into recovery, or 1-proportion of 4-12 week LC transform into >12week LC. 

``healrate-l``: >12 week LC is hard to heal, this parameter describes the annual heal rate of it. A research shows that among hospitalized patients, 68% show long covid symptoms at 6 months, and 55% show that at 2 years, this transfers to an annualized heal rate of 13.2%. 

Source: https://www.thelancet.com/journals/lanres/article/PIIS2213-2600(22)00126-6/fulltext#%20 

``infection-lc-incr``: Chance of long covid increases with each infection. This parameter describes its increment after each infection.
    
Source: https://assets.researchsquare.com/files/rs-1749502/v1/499445df-ebaf-4ab3-b30f-3028dff81fca.pdf?c=1655499468
    
``infection-lc-max``: maximal long covid chance after repeated infections

``healrate-s-decay``: This parameter describes the chance increment of short-term LC transforms to long-term LC after each infection, or the chance decrement of short-term LC heals to healthy.

``healrate-s-min``: minimal chance of short-term LC heals to healthy.

``death-rate``: death rate for acute infection if you don't have LC.

``death-rate-lc``: death rate for acute infection if you already have LC.

For realistic scenario

``python lc_calculator.py --mode realistic``

For optimistic scenario (assume humans develop some good medicine at reducing infection and LC)

``python lc_calculator.py --mode optimistic``

For pessimistic scenario (assume the virus mutates and infects more rapidly and causing higher chance of LC)

``python lc_calculator.py --mode pessimistic``

Or you can personalize parameters. You can setup a basic mode to inherent all its parameters and adjust only your adjusted params. 

For example

``python lc_calculator.py --mode realistic --infection-lc-rate 0.19``

The default mode is ``realistic``.

Sample Results under triple vaccination+BA.2-strength virus (LC: 13% per infection, 1.5% bonus per prior infection, with 65% short-term heal rate(1% decrease per prior infection) and 25% annualized long term heal rate. Death: 0.2% per infection, 1% if you already have LC)

Year 1  LC: 9.77%  Death: 0.38%

Year 2  LC: 16.00%  Death: 0.85%

Year 3  LC: 21.40%  Death: 1.38%

Year 5  LC: 30.29%  Death: 2.64%

Year 7  LC: 37.27%  Death: 4.07%

Year 10 LC: 45.19%  Death: 6.49%

For activity-limiting LC (4.5% chance per infection, 0.4% chance bonus per prior infection, 10% max per infection)

Year 1 3.47%

Year 2 5.79%

Year 3 7.90%

Year 5 11.70%

Year 7 15.08%

Year 10 19.19%

also support variants (``--mode original, delta, BA.1, BA.2, BA.5``) for calculation.
