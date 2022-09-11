# long-covid-rate-calculator

calculate the probability of you getting long covid after "living with virus" for years. 

Parameters:
``weekly-infection-rate``: The rate of you getting a new infection in any week. According to ONS data, this number averaged to be around 3% in UK in 2022. 
Source: https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/bulletins/coronaviruscovid19infectionsurveypilot/2september2022    

``infection-ic-rate``: The UK’s National Institute for Health Care and Excellence (NICE) defines COVID-19 symptom duration with three categories: <4 weeks, 4–12 weeks, and >12 weeks),with the latter two categories both considered ‘long COVID’. The rate of you getting long covid() after each infection. 

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