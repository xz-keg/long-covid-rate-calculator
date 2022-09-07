# long-covid-rate-calculator

calculate the probability of you getting long covid after "living with virus" for years. 

Parameters:
    weekly-infection-rate: The rate of you getting a new infection in any week. According to ONS data, this number averaged to be around 3% in UK in 2022. 
    Source: https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/conditionsanddiseases/bulletins/coronaviruscovid19infectionsurveypilot/2september2022
    infection-ic-rate: The UK’s National Institute for Health Care and Excellence (NICE) defines COVID-19 symptom duration with three categories: <4 weeks, 4–12 weeks, and >12 weeks),with the latter two categories both considered ‘long COVID’. The rate of you getting long covid() after each infection. 
    Source: https://www.nature.com/articles/s41467-022-30836-0
    healrate-s: short term heal rate for long covid. 

``python 