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

The three different CSV files were then joined into a single table using Pandas to ensure that the neighborhood tabulation areas that would be included into the model would have records indicating how many SHSAT were sent out to that area.  


## Choropleth of internet availability
[Link](https://wilsonchooo.github.io/Internet-Availability-on-Education/choropleth_home1.html)
[<img src="http://www.google.com.au/images/nav_logo7.png">](https://wilsonchooo.github.io/Internet-Availability-on-Education/choropleth_home1.html)

Using the Seaborn library, a heatmap was created to visualize the correlations that were present within the datasets. A positive correlation between two variables indicates that as one increases so does the other while a negative correlation occurs when a variable decreases while the other increases. The correlations can be used to test hypotheses about cause and effect relationships between the variables. While correlation may indicate that there exists a relationship between the two variables, it does not imply causation.

![Correlation Heatmap](https://wilsonchooo.github.io/Internet-Availability-on-Education/Correlation%20Heatmap.png)
From this we can quickly locate any two variables which may have a correlation with each other to look into further.



# Analysis
### Internet Adoption Rates 
The two histograms below show the amount of neighborhoods that have a certain mobile and home broadband adoption rate along with their respective averages. From this we can see how each neighborhood has a varied broadband adoption rate and the range in which they encompass.  
![Home Histogram](https://wilsonchooo.github.io/Internet-Availability-on-Education/histogram_home.png)
![Mobile Histogram](https://wilsonchooo.github.io/Internet-Availability-on-Education/histogram_mobile.png)

While the histograms allow us to see how many neighborhoods have a certain adoption rate of mobile and home broadband, a different visualization may be better suited for finding patterns such as 



You can use the [editor on GitHub](https://github.com/wilsonchooo/wilsonchooo.github.io/edit/main/index.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/wilsonchooo/wilsonchooo.github.io/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.

