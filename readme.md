# Generate customer data with Synthesized.io

Proof of concept: using the [Synthesized.io](https://www.synthesized.io/) to generate customer data 
based on the customer-data.csv file.

*** 

- To start this project you need to install synthesized (tested on the 2.7 version) 
run it and register to get your license. 
- Open **main.py** file in your favourite IDE and run it.
- It loads sample data from the **customer-data.csv** file
- New data are written in the **customer-data-new.csv** file

Model contains only one column association between person/company identity and sex columns.

***

### Known issues:

- The generic rule for numeric field with a range from 0 to 9999 doesn't work. 
Conditional Sampler expects some metadata, which is undefined.
Even when the synthesizer contains them. See lines 58, 61 and 81 in main.py file.
