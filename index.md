# Does Internet Availability Affect Education?

## Overview

The goal of this data science project was to use New York City's public data in order to find out what sort of correlation internet availability and quality has on one's education. By compiling different sources of information we can analyze the relationships that exist between these two factors. The project uses multiple python libraries in order to create the and visualize the linear regression and multi-linear models. Such libraries include matplotlib, pandas, numpy, plotly and sklearn. 

## Data Cleaning

Before we create any models or visualizations using the New York City public data we must first choose which sources of information to use and clean them up to ensure consistency, allow for fewer errors and improve data quality. 

I chose to use the following three sets of data from https://opendata.cityofnewyork.us/. 

[Internet Master Plan Adoption and Infrastructure](https://data.cityofnewyork.us/City-Government/Internet-Master-Plan-Adoption-and-Infrastructure-D/fg5j-q5nk/data)

[2017-2018 SHSAT Admissions Test Offers by Sending School](https://data.cityofnewyork.us/Education/2017-2018-SHSAT-Admissions-Test-Offers-By-Sending-/vsgi-eeb5/data)

[2017-2018 School locations](https://data.cityofnewyork.us/Education/2017-2018-School-Locations/p6h4-mpyy)

Data cleaning was performed on all three sets of data by handling any rows that had missing data, renaming columns to ensure consistency, and filtering unwanted outliers and data. 

# Summary Statistic Plots and Visualizations
The two histograms below show the amount of neighborhoods that have a certain mobile and home broadband adoption rate along with their respective averages. From this we can see how each neighborhood has had a varied broadband adoption rate and the range in which they encompass.  
![Home Histogram](https://wilsonchooo.github.io/Internet-Availability-on-Education/histogram_home.png)
![Mobile Histogram](https://wilsonchooo.github.io/Internet-Availability-on-Education/histogram_mobile.png)

We can see that the histogram based on the home broadband adoption rate has a larger variance as opposed to the mobile broadband adoption. The mobile broadband adoption rate is also roughly 10% higher than that of the home broadband.  

While the histograms allow us to see how many neighborhoods have a certain adoption rate of mobile and home broadband, a different visualization may be better suited for finding patterns such as a choropleth map.

## Choropleth of internet availability
### Home Broadband Choropleth
[<img src="https://wilsonchooo.github.io/Internet-Availability-on-Education/Home%20broadband%20choropleth.png">](https://wilsonchooo.github.io/Internet-Availability-on-Education/choropleth_home1.html)

### Mobile Broadband Choropleth
[<img src="https://wilsonchooo.github.io/Internet-Availability-on-Education/Mobile%20broadband%20choropleth.png">](https://wilsonchooo.github.io/Internet-Availability-on-Education/choropleth_mobile1.html)

From the choropleth maps we can see that home broadband adoption seems to be more unevenly distributed while the mobile broadband adoption would be more evenly distributed. The home broadband has more clusters or areas of neighborhoods which have similar adoption rates while the mobile is more streamlined throughout. From this we can infer that accessibility for mobile broadband is less dependent on what area you live in and is more accessible in general due to the averages. Home broadband also suffers from physical limitations to where you live, altering the number of providers which can supply broadband to that area. 

A choropleth map can be created to visualize the amount of residential broadband choices based on their neighborhood.

### Home Broadband Choices
[<img src="https://wilsonchooo.github.io/Internet-Availability-on-Education/Residential%20broadband%20choropleth.png">](https://wilsonchooo.github.io/Internet-Availability-on-Education/choropleth_residential_choices1.html)

# Modeling

In order to create a usable model that could accurately describe the relationship between two or more variables we need to first identify our independent variables and dependent variables. In our case, we are trying to find out if availability of internet has an effect on education through SHSAT enrollment offers. As such, we will be using the residential and mobile broadband adoption rates of a neighborhood as our metric. We will then use the 2017-2018 SHSAT offer information for each high school and categorize them into their respective neighborhoods by using the 2017-2018 School location CSV. After grouping each school into their respective neighborhood we will have the information needed in order to train and test our model. The information provided by the NYC Open data, however, does not have information pertaining to specialized enrollment for each neighborhood so we will create that ourselves by making a new column in our table and basing it off of information that we do have. 

## Correlation Heatmap
Before we create our model, a preliminary action would be to create a heatmap to see what relationships we could look into further.

Using the Seaborn library, a heatmap was created to visualize the correlations that were present within the datasets. A positive correlation between two variables indicates that as one increases so does the other while a negative correlation occurs when a variable decreases while the other increases. The correlations can be used to test hypotheses about cause and effect relationships between the variables. While correlation may indicate that there exists a relationship between the two variables, it does not imply causation.

![Correlation Heatmap](https://wilsonchooo.github.io/Internet-Availability-on-Education/Correlation%20Heatmap.png)
From this we can quickly locate any two variables which may have a correlation with each other but the ones that we are most concerned with would be "Home_Broadband_Adoption", "Mobile_Broadband_Adoption", and "Specialized Enrollment". The correlation between Home Broadband Adoption and Specialized Enrollment is .3 while Mobile Broadband Adoption and Specialized enrollment have a correlation of .008. This indicates that there is a positive correlation between these factors but that is not enough to substantiate any claims. 

We can get a better look at the relations that we previously mentioned by creating a scatter plot with a regression line using Seaborn.

### Scatter Plots
![Scatter Home](https://wilsonchooo.github.io/Internet-Availability-on-Education/scatter_home.png)
![Scatter Mobile](https://wilsonchooo.github.io/Internet-Availability-on-Education/scatter_mobile.png)

We can see that a relation does exist between the home broadband adoption and the specialized enrollment rates however it is much less apparent between the mobile broadband and the enrollment rates. In order to fit the regression line better to our underlying data we can apply a higher order polynomial regression to it. 
![Polynomial](https://wilsonchooo.github.io/Internet-Availability-on-Education/Polynomial.png)

After applying the polynomial regression onto our regression line we can see that it does indeed fit our data better and gives us a better idea of the relationship between the home broadband adoption rate and the specialized enrollment of each neighborhood. 

However, we know that our dependent variable, specialized enrollment is not solely contingent on a single factor such as the rate at which a neighborhood has adopted home broadband internet. While we could introduce a multitide of independent variables, I opted to stick to our original two of the home and mobile broadband adoption  rates to create the multiple regression with as I felt that they were the most important to answering our question.

### Multiple Linear Regression 
![Multiple Linear](https://wilsonchooo.github.io/Internet-Availability-on-Education/multiple%20linear2.png)

From the multiple linear regression created with Mobile and residential broadband adoption rates as our independent variables and specialized enrollment as our dependent variable we can see that there is a clear positive relationship between the two.

## Techniques
I used various python libaries throughout the project. Pandas was used in order to combine the tables from the NYC public data as well as clean the data and ensure consistency between the different files. For instance, the NTA or the neighborhood tabulation areas were all labeled differently in each file and they had to be changed in order to be joined together. There were also various data entries that were lacking data and they could no longer be used if it was missing in a column that was going to be used. Pandas was also used in order to calculate new rows of data that were not in the file based on existing data from other columns. Matplotlib, Seaborn and Plotly were all used to plot the different graphs. 

## Conclusion
After creating various visualizations and models in order to analyze the relationship between internet broadband adoption and specialized high school offers given for each neighborhood, it does appear that there exists a positive relationship between the two. As home and mobile broadband is adopted more, the rates of offers also goes up. However, we can not definitively say that they are based on one another as there are too many factors that could affect our metric of enrollment offers. For instance, the lack of internet adoption could be a part in something bigger such as wealth inequality or simply geographic landscape of their neighborhood disallowing for more and better broadband options. Due to this, I would not make the assumption that internet accessibility alone can determine an area's rate of SHSAT high school enrollment but I would say that it does have an effect on education in general.
