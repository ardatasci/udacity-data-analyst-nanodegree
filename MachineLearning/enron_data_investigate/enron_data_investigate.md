
# Enron Data Person of Interest Project

In 2000, Enron was one of the largest companies in the United States. By 2002, it had collapsed into bankruptcy due to widespread corporate fraud. In the resulting Federal investigation, a significant amount of typically confidential information entered into the public record, including tens of thousands of emails and detailed financial data for top executives. In this project, you will play detective, and put your new skills to use by building a person of interest identifier based on financial and email data made public as a result of the Enron scandal. To assist you in your detective work, we've combined this data with a hand-generated list of persons of interest in the fraud case, which means individuals who were indicted, reached a settlement or plea deal with the government, or testified in exchange for prosecution immunity.


In this project;

* The data were analyzed,
* NaN values in financial attributes were changed to zeros,
* Nan values in mailing features were changed to median value of related feature,
* Outliers were detected and removed from dataset,
* Features were selected based on the result of analysis in SelectKBest for classification (f_classif),
* New features were added to improve performance,
* NaiveBayes, RandomForest and AdaBoost classifiers were tried with different parameters and best classification method was chosen.



```python
#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import warnings
warnings.filterwarnings('ignore')
```


```python
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)
df = pd.DataFrame.from_dict(data_dict, orient='index')
df.head()

```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>salary</th>
      <th>to_messages</th>
      <th>deferral_payments</th>
      <th>total_payments</th>
      <th>exercised_stock_options</th>
      <th>bonus</th>
      <th>restricted_stock</th>
      <th>shared_receipt_with_poi</th>
      <th>restricted_stock_deferred</th>
      <th>total_stock_value</th>
      <th>...</th>
      <th>loan_advances</th>
      <th>from_messages</th>
      <th>other</th>
      <th>from_this_person_to_poi</th>
      <th>poi</th>
      <th>director_fees</th>
      <th>deferred_income</th>
      <th>long_term_incentive</th>
      <th>email_address</th>
      <th>from_poi_to_this_person</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>ALLEN PHILLIP K</th>
      <td>201955</td>
      <td>2902</td>
      <td>2869717</td>
      <td>4484442</td>
      <td>1729541</td>
      <td>4175000</td>
      <td>126027</td>
      <td>1407</td>
      <td>-126027</td>
      <td>1729541</td>
      <td>...</td>
      <td>NaN</td>
      <td>2195</td>
      <td>152</td>
      <td>65</td>
      <td>False</td>
      <td>NaN</td>
      <td>-3081055</td>
      <td>304805</td>
      <td>phillip.allen@enron.com</td>
      <td>47</td>
    </tr>
    <tr>
      <th>BADUM JAMES P</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>178980</td>
      <td>182466</td>
      <td>257817</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>257817</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>False</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>BANNANTINE JAMES M</th>
      <td>477</td>
      <td>566</td>
      <td>NaN</td>
      <td>916197</td>
      <td>4046157</td>
      <td>NaN</td>
      <td>1757552</td>
      <td>465</td>
      <td>-560222</td>
      <td>5243487</td>
      <td>...</td>
      <td>NaN</td>
      <td>29</td>
      <td>864523</td>
      <td>0</td>
      <td>False</td>
      <td>NaN</td>
      <td>-5104</td>
      <td>NaN</td>
      <td>james.bannantine@enron.com</td>
      <td>39</td>
    </tr>
    <tr>
      <th>BAXTER JOHN C</th>
      <td>267102</td>
      <td>NaN</td>
      <td>1295738</td>
      <td>5634343</td>
      <td>6680544</td>
      <td>1200000</td>
      <td>3942714</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>10623258</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2660303</td>
      <td>NaN</td>
      <td>False</td>
      <td>NaN</td>
      <td>-1386055</td>
      <td>1586055</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>BAY FRANKLIN R</th>
      <td>239671</td>
      <td>NaN</td>
      <td>260455</td>
      <td>827696</td>
      <td>NaN</td>
      <td>400000</td>
      <td>145796</td>
      <td>NaN</td>
      <td>-82782</td>
      <td>63014</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>69</td>
      <td>NaN</td>
      <td>False</td>
      <td>NaN</td>
      <td>-201641</td>
      <td>NaN</td>
      <td>frank.bay@enron.com</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 21 columns</p>
</div>



There NaN values in some features of the dataset, for simplification of the analysis, these NaN strings shall be replaced with null values. 


```python
df = df.replace('NaN', np.nan)
```

### Dataset Analysis & Wrangling


```python
print "# of investigated people: ", df['poi'].count()
print "Person of interest distirbution: ", df.groupby('poi')['poi'].count()
print "Initial feature set: ", df.shape[1]
```

    # of investigated people:  146
    Person of interest distirbution:  poi
    False    128
    True      18
    Name: poi, dtype: int64
    Initial feature set:  21


There are 146 people, 18 of which is labeled as person of interes in the dataset. There are total of 21 features which are categorized into 2 groups, financial and mailing features.


```python
print 'NaN values of features'
df.isnull().sum()
```

    NaN values of features





    salary                        51
    to_messages                   60
    deferral_payments            107
    total_payments                21
    exercised_stock_options       44
    bonus                         64
    restricted_stock              36
    shared_receipt_with_poi       60
    restricted_stock_deferred    128
    total_stock_value             20
    expenses                      51
    loan_advances                142
    from_messages                 60
    other                         53
    from_this_person_to_poi       60
    poi                            0
    director_fees                129
    deferred_income               97
    long_term_incentive           80
    email_address                 35
    from_poi_to_this_person       60
    dtype: int64



Missing financial features can be filled with zeros since they are related with amount of money. 


```python
financial_features = ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees']
df[financial_features] = df[financial_features].fillna(0)
```

Missing values in mailing features are very interesting since the possibility of those people to have received or sent any email is very low. If those values were filled with zeros, in classification phase those values may effect the success of the method. Therefore, filling with average values seems more logical. 


```python
email_features = ['to_messages', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi']
df[email_features] = df[email_features].fillna(df[email_features].median())
df.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>salary</th>
      <th>to_messages</th>
      <th>deferral_payments</th>
      <th>total_payments</th>
      <th>exercised_stock_options</th>
      <th>bonus</th>
      <th>restricted_stock</th>
      <th>shared_receipt_with_poi</th>
      <th>restricted_stock_deferred</th>
      <th>total_stock_value</th>
      <th>...</th>
      <th>loan_advances</th>
      <th>from_messages</th>
      <th>other</th>
      <th>from_this_person_to_poi</th>
      <th>poi</th>
      <th>director_fees</th>
      <th>deferred_income</th>
      <th>long_term_incentive</th>
      <th>email_address</th>
      <th>from_poi_to_this_person</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>ALLEN PHILLIP K</th>
      <td>201955.0</td>
      <td>2902.0</td>
      <td>2869717.0</td>
      <td>4484442.0</td>
      <td>1729541.0</td>
      <td>4175000.0</td>
      <td>126027.0</td>
      <td>1407.0</td>
      <td>-126027.0</td>
      <td>1729541.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>2195.0</td>
      <td>152.0</td>
      <td>65.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>-3081055.0</td>
      <td>304805.0</td>
      <td>phillip.allen@enron.com</td>
      <td>47.0</td>
    </tr>
    <tr>
      <th>BADUM JAMES P</th>
      <td>0.0</td>
      <td>1211.0</td>
      <td>178980.0</td>
      <td>182466.0</td>
      <td>257817.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>740.5</td>
      <td>0.0</td>
      <td>257817.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>41.0</td>
      <td>0.0</td>
      <td>8.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>35.0</td>
    </tr>
    <tr>
      <th>BANNANTINE JAMES M</th>
      <td>477.0</td>
      <td>566.0</td>
      <td>0.0</td>
      <td>916197.0</td>
      <td>4046157.0</td>
      <td>0.0</td>
      <td>1757552.0</td>
      <td>465.0</td>
      <td>-560222.0</td>
      <td>5243487.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>29.0</td>
      <td>864523.0</td>
      <td>0.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>-5104.0</td>
      <td>0.0</td>
      <td>james.bannantine@enron.com</td>
      <td>39.0</td>
    </tr>
    <tr>
      <th>BAXTER JOHN C</th>
      <td>267102.0</td>
      <td>1211.0</td>
      <td>1295738.0</td>
      <td>5634343.0</td>
      <td>6680544.0</td>
      <td>1200000.0</td>
      <td>3942714.0</td>
      <td>740.5</td>
      <td>0.0</td>
      <td>10623258.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>41.0</td>
      <td>2660303.0</td>
      <td>8.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>-1386055.0</td>
      <td>1586055.0</td>
      <td>NaN</td>
      <td>35.0</td>
    </tr>
    <tr>
      <th>BAY FRANKLIN R</th>
      <td>239671.0</td>
      <td>1211.0</td>
      <td>260455.0</td>
      <td>827696.0</td>
      <td>0.0</td>
      <td>400000.0</td>
      <td>145796.0</td>
      <td>740.5</td>
      <td>-82782.0</td>
      <td>63014.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>41.0</td>
      <td>69.0</td>
      <td>8.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>-201641.0</td>
      <td>0.0</td>
      <td>frank.bay@enron.com</td>
      <td>35.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 21 columns</p>
</div>



### Outlier Analysis


```python
df.describe()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>salary</th>
      <th>to_messages</th>
      <th>deferral_payments</th>
      <th>total_payments</th>
      <th>exercised_stock_options</th>
      <th>bonus</th>
      <th>restricted_stock</th>
      <th>shared_receipt_with_poi</th>
      <th>restricted_stock_deferred</th>
      <th>total_stock_value</th>
      <th>expenses</th>
      <th>loan_advances</th>
      <th>from_messages</th>
      <th>other</th>
      <th>from_this_person_to_poi</th>
      <th>director_fees</th>
      <th>deferred_income</th>
      <th>long_term_incentive</th>
      <th>from_poi_to_this_person</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>1.460000e+02</td>
      <td>146.000000</td>
      <td>1.460000e+02</td>
      <td>1.460000e+02</td>
      <td>1.460000e+02</td>
      <td>1.460000e+02</td>
      <td>1.460000e+02</td>
      <td>146.000000</td>
      <td>1.460000e+02</td>
      <td>1.460000e+02</td>
      <td>1.460000e+02</td>
      <td>1.460000e+02</td>
      <td>146.000000</td>
      <td>1.460000e+02</td>
      <td>146.000000</td>
      <td>1.460000e+02</td>
      <td>1.460000e+02</td>
      <td>1.460000e+02</td>
      <td>146.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>3.658114e+05</td>
      <td>1719.260274</td>
      <td>4.387965e+05</td>
      <td>4.350622e+06</td>
      <td>4.182736e+06</td>
      <td>1.333474e+06</td>
      <td>1.749257e+06</td>
      <td>997.301370</td>
      <td>2.051637e+04</td>
      <td>5.846018e+06</td>
      <td>7.074827e+04</td>
      <td>1.149658e+06</td>
      <td>375.452055</td>
      <td>5.854318e+05</td>
      <td>27.575342</td>
      <td>1.942249e+04</td>
      <td>-3.827622e+05</td>
      <td>6.646839e+05</td>
      <td>52.609589</td>
    </tr>
    <tr>
      <th>std</th>
      <td>2.203575e+06</td>
      <td>2022.788673</td>
      <td>2.741325e+06</td>
      <td>2.693448e+07</td>
      <td>2.607040e+07</td>
      <td>8.094029e+06</td>
      <td>1.089995e+07</td>
      <td>927.488807</td>
      <td>1.439661e+06</td>
      <td>3.624681e+07</td>
      <td>4.327163e+05</td>
      <td>9.649342e+06</td>
      <td>1437.174998</td>
      <td>3.682345e+06</td>
      <td>78.357081</td>
      <td>1.190543e+05</td>
      <td>2.378250e+06</td>
      <td>4.046072e+06</td>
      <td>68.210867</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000e+00</td>
      <td>57.000000</td>
      <td>-1.025000e+05</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>-2.604490e+06</td>
      <td>2.000000</td>
      <td>-7.576788e+06</td>
      <td>-4.409300e+04</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>12.000000</td>
      <td>0.000000e+00</td>
      <td>0.000000</td>
      <td>0.000000e+00</td>
      <td>-2.799289e+07</td>
      <td>0.000000e+00</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>0.000000e+00</td>
      <td>904.250000</td>
      <td>0.000000e+00</td>
      <td>9.394475e+04</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>8.115000e+03</td>
      <td>591.500000</td>
      <td>0.000000e+00</td>
      <td>2.288695e+05</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>36.000000</td>
      <td>0.000000e+00</td>
      <td>6.000000</td>
      <td>0.000000e+00</td>
      <td>-3.792600e+04</td>
      <td>0.000000e+00</td>
      <td>25.750000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>2.105960e+05</td>
      <td>1211.000000</td>
      <td>0.000000e+00</td>
      <td>9.413595e+05</td>
      <td>6.082935e+05</td>
      <td>3.000000e+05</td>
      <td>3.605280e+05</td>
      <td>740.500000</td>
      <td>0.000000e+00</td>
      <td>9.659550e+05</td>
      <td>2.018200e+04</td>
      <td>0.000000e+00</td>
      <td>41.000000</td>
      <td>9.595000e+02</td>
      <td>8.000000</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>35.000000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>2.708505e+05</td>
      <td>1585.750000</td>
      <td>9.684500e+03</td>
      <td>1.968287e+06</td>
      <td>1.714221e+06</td>
      <td>8.000000e+05</td>
      <td>8.145280e+05</td>
      <td>893.500000</td>
      <td>0.000000e+00</td>
      <td>2.319991e+06</td>
      <td>5.374075e+04</td>
      <td>0.000000e+00</td>
      <td>51.250000</td>
      <td>1.506065e+05</td>
      <td>13.750000</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>3.750648e+05</td>
      <td>40.750000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>2.670423e+07</td>
      <td>15149.000000</td>
      <td>3.208340e+07</td>
      <td>3.098866e+08</td>
      <td>3.117640e+08</td>
      <td>9.734362e+07</td>
      <td>1.303223e+08</td>
      <td>5521.000000</td>
      <td>1.545629e+07</td>
      <td>4.345095e+08</td>
      <td>5.235198e+06</td>
      <td>8.392500e+07</td>
      <td>14368.000000</td>
      <td>4.266759e+07</td>
      <td>609.000000</td>
      <td>1.398517e+06</td>
      <td>0.000000e+00</td>
      <td>4.852193e+07</td>
      <td>528.000000</td>
    </tr>
  </tbody>
</table>
</div>




```python
def plot_dataframe(dataframe):
    fig = plt.figure(figsize = (25,10))
    ax = fig.gca()
    pd.options.display.mpl_style = 'default'
    dataframe.boxplot(rot=45)
    
plot_dataframe(df[financial_features])

```


![png](output_15_0.png)


There are extreme outliers in the dataset which can be seen in total_stock_value, total_payments and excersized_stock_options. Let's see those outliers.



```python
df[(df.total_stock_value > 4e8) | (df.total_payments > 3e8) | (df.exercised_stock_options > 3e8) ]
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>salary</th>
      <th>to_messages</th>
      <th>deferral_payments</th>
      <th>total_payments</th>
      <th>exercised_stock_options</th>
      <th>bonus</th>
      <th>restricted_stock</th>
      <th>shared_receipt_with_poi</th>
      <th>restricted_stock_deferred</th>
      <th>total_stock_value</th>
      <th>...</th>
      <th>loan_advances</th>
      <th>from_messages</th>
      <th>other</th>
      <th>from_this_person_to_poi</th>
      <th>poi</th>
      <th>director_fees</th>
      <th>deferred_income</th>
      <th>long_term_incentive</th>
      <th>email_address</th>
      <th>from_poi_to_this_person</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>TOTAL</th>
      <td>26704229.0</td>
      <td>1211.0</td>
      <td>32083396.0</td>
      <td>309886585.0</td>
      <td>311764000.0</td>
      <td>97343619.0</td>
      <td>130322299.0</td>
      <td>740.5</td>
      <td>-7576788.0</td>
      <td>434509511.0</td>
      <td>...</td>
      <td>83925000.0</td>
      <td>41.0</td>
      <td>42667589.0</td>
      <td>8.0</td>
      <td>False</td>
      <td>1398517.0</td>
      <td>-27992891.0</td>
      <td>48521928.0</td>
      <td>NaN</td>
      <td>35.0</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 21 columns</p>
</div>



It is clearly seen that 'TOTAL' is an extreme outlier as expected since this is datapoint that shows the cumulative values in the dataset and does not represent a real user.


```python
df = df.drop('TOTAL')
plot_dataframe(df[financial_features])
```


![png](output_19_0.png)


Now lets see mailing features whether if they contain any outliers.


```python
plot_dataframe(df[email_features])
```


![png](output_21_0.png)



```python
df[(df.to_messages > 6000) | (df.from_messages > 1000) ]
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>salary</th>
      <th>to_messages</th>
      <th>deferral_payments</th>
      <th>total_payments</th>
      <th>exercised_stock_options</th>
      <th>bonus</th>
      <th>restricted_stock</th>
      <th>shared_receipt_with_poi</th>
      <th>restricted_stock_deferred</th>
      <th>total_stock_value</th>
      <th>...</th>
      <th>loan_advances</th>
      <th>from_messages</th>
      <th>other</th>
      <th>from_this_person_to_poi</th>
      <th>poi</th>
      <th>director_fees</th>
      <th>deferred_income</th>
      <th>long_term_incentive</th>
      <th>email_address</th>
      <th>from_poi_to_this_person</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>ALLEN PHILLIP K</th>
      <td>201955.0</td>
      <td>2902.0</td>
      <td>2869717.0</td>
      <td>4484442.0</td>
      <td>1729541.0</td>
      <td>4175000.0</td>
      <td>126027.0</td>
      <td>1407.0</td>
      <td>-126027.0</td>
      <td>1729541.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>2195.0</td>
      <td>152.0</td>
      <td>65.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>-3081055.0</td>
      <td>304805.0</td>
      <td>phillip.allen@enron.com</td>
      <td>47.0</td>
    </tr>
    <tr>
      <th>BECK SALLY W</th>
      <td>231330.0</td>
      <td>7315.0</td>
      <td>0.0</td>
      <td>969068.0</td>
      <td>0.0</td>
      <td>700000.0</td>
      <td>126027.0</td>
      <td>2639.0</td>
      <td>0.0</td>
      <td>126027.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>4343.0</td>
      <td>566.0</td>
      <td>386.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>sally.beck@enron.com</td>
      <td>144.0</td>
    </tr>
    <tr>
      <th>BELDEN TIMOTHY N</th>
      <td>213999.0</td>
      <td>7991.0</td>
      <td>2144013.0</td>
      <td>5501630.0</td>
      <td>953136.0</td>
      <td>5249999.0</td>
      <td>157569.0</td>
      <td>5521.0</td>
      <td>0.0</td>
      <td>1110705.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>484.0</td>
      <td>210698.0</td>
      <td>108.0</td>
      <td>True</td>
      <td>0.0</td>
      <td>-2334434.0</td>
      <td>0.0</td>
      <td>tim.belden@enron.com</td>
      <td>228.0</td>
    </tr>
    <tr>
      <th>BUY RICHARD B</th>
      <td>330546.0</td>
      <td>3523.0</td>
      <td>649584.0</td>
      <td>2355702.0</td>
      <td>2542813.0</td>
      <td>900000.0</td>
      <td>901657.0</td>
      <td>2333.0</td>
      <td>0.0</td>
      <td>3444470.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>1053.0</td>
      <td>400572.0</td>
      <td>71.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>-694862.0</td>
      <td>769862.0</td>
      <td>rick.buy@enron.com</td>
      <td>156.0</td>
    </tr>
    <tr>
      <th>DELAINEY DAVID W</th>
      <td>365163.0</td>
      <td>3093.0</td>
      <td>0.0</td>
      <td>4747979.0</td>
      <td>2291113.0</td>
      <td>3000000.0</td>
      <td>1323148.0</td>
      <td>2097.0</td>
      <td>0.0</td>
      <td>3614261.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>3069.0</td>
      <td>1661.0</td>
      <td>609.0</td>
      <td>True</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1294981.0</td>
      <td>david.delainey@enron.com</td>
      <td>66.0</td>
    </tr>
    <tr>
      <th>HAEDICKE MARK E</th>
      <td>374125.0</td>
      <td>4009.0</td>
      <td>2157527.0</td>
      <td>3859065.0</td>
      <td>608750.0</td>
      <td>1150000.0</td>
      <td>524169.0</td>
      <td>1847.0</td>
      <td>-329825.0</td>
      <td>803094.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>1941.0</td>
      <td>52382.0</td>
      <td>61.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>-934484.0</td>
      <td>983346.0</td>
      <td>mark.haedicke@enron.com</td>
      <td>180.0</td>
    </tr>
    <tr>
      <th>HAYSLETT RODERICK J</th>
      <td>0.0</td>
      <td>2649.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>346663.0</td>
      <td>571.0</td>
      <td>0.0</td>
      <td>346663.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>1061.0</td>
      <td>0.0</td>
      <td>38.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>rod.hayslett@enron.com</td>
      <td>35.0</td>
    </tr>
    <tr>
      <th>HORTON STANLEY C</th>
      <td>0.0</td>
      <td>2350.0</td>
      <td>3131860.0</td>
      <td>3131860.0</td>
      <td>5210569.0</td>
      <td>0.0</td>
      <td>2046079.0</td>
      <td>1074.0</td>
      <td>0.0</td>
      <td>7256648.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>1073.0</td>
      <td>0.0</td>
      <td>15.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>stanley.horton@enron.com</td>
      <td>44.0</td>
    </tr>
    <tr>
      <th>KAMINSKI WINCENTY J</th>
      <td>275101.0</td>
      <td>4607.0</td>
      <td>0.0</td>
      <td>1086821.0</td>
      <td>850010.0</td>
      <td>400000.0</td>
      <td>126027.0</td>
      <td>583.0</td>
      <td>0.0</td>
      <td>976037.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>14368.0</td>
      <td>4669.0</td>
      <td>171.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>323466.0</td>
      <td>vince.kaminski@enron.com</td>
      <td>41.0</td>
    </tr>
    <tr>
      <th>KEAN STEVEN J</th>
      <td>404338.0</td>
      <td>12754.0</td>
      <td>0.0</td>
      <td>1747522.0</td>
      <td>2022048.0</td>
      <td>1000000.0</td>
      <td>4131594.0</td>
      <td>3639.0</td>
      <td>0.0</td>
      <td>6153642.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>6759.0</td>
      <td>1231.0</td>
      <td>387.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>300000.0</td>
      <td>steven.kean@enron.com</td>
      <td>140.0</td>
    </tr>
    <tr>
      <th>KITCHEN LOUISE</th>
      <td>271442.0</td>
      <td>8305.0</td>
      <td>0.0</td>
      <td>3471141.0</td>
      <td>81042.0</td>
      <td>3100000.0</td>
      <td>466101.0</td>
      <td>3669.0</td>
      <td>0.0</td>
      <td>547143.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>1728.0</td>
      <td>93925.0</td>
      <td>194.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>louise.kitchen@enron.com</td>
      <td>251.0</td>
    </tr>
    <tr>
      <th>LAVORATO JOHN J</th>
      <td>339288.0</td>
      <td>7259.0</td>
      <td>0.0</td>
      <td>10425757.0</td>
      <td>4158995.0</td>
      <td>8000000.0</td>
      <td>1008149.0</td>
      <td>3962.0</td>
      <td>0.0</td>
      <td>5167144.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>2585.0</td>
      <td>1552.0</td>
      <td>411.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>2035380.0</td>
      <td>john.lavorato@enron.com</td>
      <td>528.0</td>
    </tr>
    <tr>
      <th>MCCONNELL MICHAEL S</th>
      <td>365038.0</td>
      <td>3329.0</td>
      <td>0.0</td>
      <td>2101364.0</td>
      <td>1623010.0</td>
      <td>1100000.0</td>
      <td>1478269.0</td>
      <td>2189.0</td>
      <td>0.0</td>
      <td>3101279.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>2742.0</td>
      <td>540.0</td>
      <td>194.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>554422.0</td>
      <td>mike.mcconnell@enron.com</td>
      <td>92.0</td>
    </tr>
    <tr>
      <th>SHANKMAN JEFFREY A</th>
      <td>304110.0</td>
      <td>3221.0</td>
      <td>0.0</td>
      <td>3038702.0</td>
      <td>1441898.0</td>
      <td>2000000.0</td>
      <td>630137.0</td>
      <td>1730.0</td>
      <td>0.0</td>
      <td>2072035.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>2681.0</td>
      <td>1191.0</td>
      <td>83.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>554422.0</td>
      <td>jeffrey.shankman@enron.com</td>
      <td>94.0</td>
    </tr>
    <tr>
      <th>SHAPIRO RICHARD S</th>
      <td>269076.0</td>
      <td>15149.0</td>
      <td>0.0</td>
      <td>1057548.0</td>
      <td>607837.0</td>
      <td>650000.0</td>
      <td>379164.0</td>
      <td>4527.0</td>
      <td>0.0</td>
      <td>987001.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>1215.0</td>
      <td>705.0</td>
      <td>65.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>richard.shapiro@enron.com</td>
      <td>74.0</td>
    </tr>
    <tr>
      <th>WHALLEY LAWRENCE G</th>
      <td>510364.0</td>
      <td>6019.0</td>
      <td>0.0</td>
      <td>4677574.0</td>
      <td>3282960.0</td>
      <td>3000000.0</td>
      <td>2796177.0</td>
      <td>3920.0</td>
      <td>0.0</td>
      <td>6079137.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>556.0</td>
      <td>301026.0</td>
      <td>24.0</td>
      <td>False</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>808346.0</td>
      <td>greg.whalley@enron.com</td>
      <td>186.0</td>
    </tr>
  </tbody>
</table>
<p>16 rows × 21 columns</p>
</div>



There are outliers in mailing features, some people may have received or sent much more emails than the others. I do not think they are extreme outliers, however removing those datapoints will effect the distribution of the dataset postively.


```python
df = df[df.to_messages < 6000]
df = df[df.from_messages < 1000]
```

### Feature Selection & Engineering

After wrangling phase, features that are more descriptive than the others will be selected in feature selection phase using scikit SelectKBest function. Since the aim is classification, f_classif method will be used to extract more descriptive features on the target feature.

REF: http://scikit-learn.org/stable/modules/feature_selection.html


```python
from sklearn.feature_selection import SelectKBest, f_classif

filtered_features_df = df.drop(['poi', 'email_address'], axis=1)
target_feature = df.poi

feature_selector = SelectKBest(f_classif)
feature_selector.fit(filtered_features_df, target_feature)
# Get idxs of columns to keep
idxs_selected = feature_selector.get_support(indices=True)
features_dataframe_new = filtered_features_df[idxs_selected]
selected_features = list(features_dataframe_new)
print selected_features
```

    ['salary', 'to_messages', 'exercised_stock_options', 'bonus', 'restricted_stock', 'shared_receipt_with_poi', 'total_stock_value', 'from_this_person_to_poi', 'deferred_income', 'long_term_incentive']


10 of 21 features were selected for classification methods based on SelectKBest function results.

After feature selection, those features will be engineered in order to improve the classification methods success.



```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import cross_val_score, StratifiedKFold, StratifiedShuffleSplit
from sklearn.metrics import classification_report, make_scorer, accuracy_score, precision_score, recall_score, f1_score



def evaluate_classifier(clf, X, y):
    cv = StratifiedShuffleSplit(y, 100, random_state=42)
    print 'accuracy', cross_val_score(clf, X, y, cv=cv).mean()
    print 'precision', cross_val_score(clf, X, y, scoring=make_scorer(precision_score), cv=cv).mean()
    print 'recall', cross_val_score(clf, X, y, scoring=make_scorer(recall_score), cv=cv).mean()
    

def try_classifiers(X, y):
    print "GaussianNB Results"
    clf = GaussianNB()
    evaluate_classifier(clf, X, y)
    print
    
    print "DecisionTree Results"
    clf = DecisionTreeClassifier(random_state=42)
    evaluate_classifier(clf, X, y)
    print
    
    print "RandomForestClassifier Results"
    clf = RandomForestClassifier(random_state=42)
    evaluate_classifier(clf, X, y)
    print
    
    
    
X = df[selected_features]
y = df.poi
try_classifiers(X, y)
```

    GaussianNB Results
    accuracy 0.827692307692
    precision 0.357333333333
    recall 0.35
    
    DecisionTree Results
    accuracy 0.786153846154
    precision 0.215
    recall 0.24
    
    RandomForestClassifier Results
    accuracy 0.816923076923
    precision 0.171666666667
    recall 0.14
    


Selected features were ['salary', 'to_messages', 'exercised_stock_options', 'bonus', 'restricted_stock', 'shared_receipt_with_poi', 'total_stock_value', 'from_this_person_to_poi', 'deferred_income', 'from_poi_to_this_person'].

I will engineer the mailing features as follows :

* to_message_poi_ratio = from_this_person_to_poi / to_messages
* from_message_poi_ratio = from_poi_to_this_person / from_messages
* message_in_out_ratio = from_messages / to_messages



```python
df['to_message_poi_ratio'] = df['from_this_person_to_poi'] / df['to_messages']
df['from_message_poi_ratio'] = df['from_poi_to_this_person'] / df['from_messages']
df['message_in_out_ratio'] = df['from_messages'] / df['to_messages']


engineered_features = selected_features + ['from_message_poi_ratio', 'message_in_out_ratio', 'to_message_poi_ratio']
dropped_features = ['from_this_person_to_poi', 'to_messages']

def created_engineered_dataframe(engineered_f, dropped_f, data_frame):
    X_engineered = data_frame[engineered_features]
    X_engineered = X_engineered.drop(dropped_features, axis=1)
    return X_engineered

X = created_engineered_dataframe(engineered_features, dropped_features, df)
y = df.poi
try_classifiers(X, y)


```

    GaussianNB Results
    accuracy 0.839230769231
    precision 0.3925
    recall 0.365
    
    DecisionTree Results
    accuracy 0.803076923077
    precision 0.300166666667
    recall 0.305
    
    RandomForestClassifier Results
    accuracy 0.842307692308
    precision 0.301666666667
    recall 0.2
    


### Parameter Tuning

NaiveBayes results lower than Random Forest and AdaBoost models. Therefore, parameter tuninig is applied for Random Forest and Ada Boost models.

For random forest, criterion, min_samples_leaf, max_features and max_depth parameters were tried using grid search. Best results were seen in below parameter options: 

{'max_features': 2, 'min_samples_split': 4, 'criterion': 'entropy', 'max_depth': 5, 'min_samples_leaf': 1}



```python
from sklearn.grid_search import GridSearchCV


grid = {
    'criterion':('gini', 'entropy'),
    'min_samples_split':[2,4],
    'min_samples_leaf':range(1, 50, 5),
    'max_features':range(1,10),
    'max_depth': range(1, 10)
}

search = GridSearchCV(RandomForestClassifier(random_state=42),
                      grid, make_scorer(f1_score), cv=StratifiedKFold(y), n_jobs=-1)
search.fit(X, y)

print search.best_score_
print search.best_params_

evaluate_classifier(search.best_estimator_, X, y)
```

    0.35535868094
    {'max_features': 2, 'min_samples_split': 4, 'criterion': 'entropy', 'max_depth': 5, 'min_samples_leaf': 1}
    accuracy 0.85
    precision 0.286666666667
    recall 0.195


For Decision Tree, best estimator criterion, best results were seen in below parameter options: 

{'criterion': 'entropy', 'max_depth': 5, 'min_samples_leaf': 1}


```python
grid = {
    'criterion': ('gini', 'entropy'),
    'min_samples_leaf':range(1, 50, 5),
    'max_depth': range(1, 10)
}

search = GridSearchCV(DecisionTreeClassifier(random_state=42),
                      grid, make_scorer(f1_score), cv=StratifiedKFold(y), n_jobs=-1)
search.fit(X, y)
print search.best_score_
print search.best_params_

evaluate_classifier(search.best_estimator_, X, y)
```

    0.340051679587
    {'criterion': 'entropy', 'max_depth': 5, 'min_samples_leaf': 1}
    accuracy 0.809230769231
    precision 0.35669047619
    recall 0.34


As a classification method, I choose Decision Tree with parameters {'criterion': 'entropy', 'max_depth': 5, 'min_samples_leaf': 1} since it gave the highest accuracy, (precision and recall > .3).


tester.py results are as below:

DecisionTreeClassifier(class_weight=None, criterion='entropy', max_depth=5,
            max_features=None, max_leaf_nodes=None,
            min_impurity_split=1e-07, min_samples_leaf=1,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            presort=False, random_state=43, splitter='best')
            
            
       Accuracy: 0.77786       
       Precision: 0.31413     
       Recall: 0.46900 
       F1: 0.37625     
       F2: 0.42691
       Total predictions: 7000 
       True positives:  469    
       False positives: 1024   
       False negatives:  531   
       True negatives: 4976
        
