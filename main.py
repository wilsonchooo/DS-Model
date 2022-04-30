
"""
Name:       Wilson Cho
Email:      wilson.cho74@myhunter.cuny.edu
Resources:  https://www.textbook.ds100.org/ch/20/feature_polynomial.html?highlight=polynomial
            https://www.textbook.ds100.org/ch/09/wrangling_structure.html
            https://www.textbook.ds100.org/ch/11/viz_scale.html
            https://seaborn.pydata.org/tutorial/regression.html
            https://plotly.com/python/choropleth-maps/
            https://stackoverflow.com/questions/65888553/fitting-a-line-through-3d-x-y-z-scatter-plot-data,
Title:      Internet-Availability-on-Education
URL:        https://wilsonchooo.github.io/Internet-Availability-on-Education/
"""
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import json
from area import area
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.decomposition import PCA

#Reads the csv file containing the internet master plan adoption and infrascture data from NYC open data. 
def make_internet_df(internet_file):
    internet_df = pd.read_csv(internet_file)
    #takes in these specific columns as they seem to be applicable to our project
    cols = ["Neighborhood Tabulation Area Code (NTA Code)",
            "Home Broadband Adoption by Quartiles (High, Medium-High, Medium-Low, Low)",
            "Neighborhood Tabulation Area Name (NTA NAME)",
            "Borough Name","Total Population",
            "Population Density (per Sq. Mi.)",
            "NYC Internet Master Plan Open Access Infrastructure Cost Comparison Coefficient",
            "Number of Fixed Wireless Providers Available","Percentage of Households with fewer than 3 broadband options available",
            "Total Number of Households","Home Broadband Adoption (Percentage of Households)","Mobile Broadband Adoption (Percentage of Households)",
            "Mobile Dependent Households (Percentage of Households)","Number of Households","Households Receiving Benefits","Low-Income Housing (NYCHA)",
            "Residential Broadband Choice Average by NTA"]
    internet_df = internet_df[cols]
    #Rename some of the columns
    internet_df = internet_df.rename(columns={'Neighborhood Tabulation Area Code (NTA Code)': 'NTA_CODE', 
                                            'Neighborhood Tabulation Area Name (NTA NAME)': 'NTA_NAME', 
                                            "Borough Name":'Borough',
                                            "Total Population":"Total_Population",
                                            "Population Density (per Sq. Mi.)":"Population_Density",
                                            "Mobile Broadband Adoption (Percentage of Households)":"Mobile_Broadband_Adoption",
                                            "Home Broadband Adoption (Percentage of Households)":"Home_Broadband_Adoption" })    
    #Remove any rows that are missing data from the specified rows 
    internet_df = internet_df.dropna(subset=["Home_Broadband_Adoption", "Mobile_Broadband_Adoption","Borough","Total_Population", "NTA_CODE", "NTA_NAME"])
    return internet_df

def make_school_df(shsat_file,schools_file):
    #Read both the SHSAT enrollment data as well as the school location data
    shsat_df = pd.read_csv(shsat_file)
    #Ensure that our keys are of the same type for when they are joined later.
    shsat_df['Feeder School DBN'] = shsat_df['Feeder School DBN'].astype(str)
    shsat_df = shsat_df.rename(columns={'Feeder School DBN':'School_code'})
    
    schools_df = pd.read_csv(schools_file)
    #Get specific columns from the csv
    schools_df = schools_df[["NTA","NTA_NAME","LOCATION_CATEGORY_DESCRIPTION","LOCATION_NAME","LOCATION_CODE","ATS SYSTEM CODE",]]
    schools_df["ATS SYSTEM CODE"] = schools_df["ATS SYSTEM CODE"].astype(str)
    schools_df = schools_df.rename(columns={"ATS SYSTEM CODE":'School_code'})
    schools_df['School_code'] = schools_df['School_code'].str.strip()

    #inner join both the dataframes to create a single dataframe that will contain both the school and information about where they are stored.
    #Additionally keeps only information about schools that have SHSAT offers.
    df = pd.merge(shsat_df,schools_df,how="inner",on="School_code")
    df = df.dropna()
    return df 

def combine_df(internet_df,school_df):
    #Groups up the schools by NTA and sums up their values.
    nta_sat = school_df.groupby('NTA').sum()
    #Left join on the summed up schools and 
    internet_sat = pd.merge(internet_df,nta_sat,how='left',left_on="NTA_CODE",right_on="NTA")
    internet_sat = internet_sat.dropna(subset=["Count of Students in HS Admissions", "Count of Testers", "Count of Offers"])

    #internet_sat["Specialized Enrollment"] = internet_sat["Count of Offers"]/internet_sat["Count of Testers"]
    internet_sat["Specialized Enrollment"] = internet_sat["Count of Offers"]/internet_sat["Count of Students in HS Admissions"]
    
    internet_sat["Mobile_Broadband_Adoption"] = internet_sat["Mobile_Broadband_Adoption"].astype(float)
    internet_sat["Home_Broadband_Adoption"] = internet_sat["Home_Broadband_Adoption"].astype(float)
    #internet_sat["benefits"] = internet_sat["Households Receiving Benefits"]/internet_sat["Number of Households"]


    return internet_sat

def heatmap(df):
    #set attributes of matplotlib for styling
    plt.figure(figsize=(14,8))
    sns.set_theme(style="white")
    sns.set(style="ticks")
    ax = plt.axes()
    #create a new dataframe with the correlations of the original df 
    correlated_df = df.corr()
    #createa heatmap using the correlated df and seaborn.
    heatmap = sns.heatmap(correlated_df, annot=True, cmap="Blues", fmt='.1g', ax=ax)
    plt.show()


def histogram(df,type):
    #set attributes of matplotlib for styling
    plt.figure(figsize=(14,8))
    sns.set_theme(style="white")
    sns.set(style="ticks")
    ax = plt.axes()
    #Create histograms based on whether type is based on thr parameters.
    if (type == "home"):
        avg = str(round(df["Home_Broadband_Adoption"].mean(),3))
        print(df["Home_Broadband_Adoption"].count())
        ax.set_title(f'Home Broadband Adoption Rates by Neighborhood \n Average = {avg}')
        hist = sns.histplot(data = df, x="Home_Broadband_Adoption", bins=80, color='navy',alpha = .6,kde=True)
        hist.set_xlabel(r"Home Broadband Adoption in %")
        hist.set_ylabel(r"Number of Neighborhoods")
    elif (type == "mobile"):
        avg = str(round(df["Mobile_Broadband_Adoption"].mean(),3))
        print(df["Mobile_Broadband_Adoption"].count())
        ax.set_title(f'Mobile Broadband Adoption Rates by Neighborhood \n Average = {avg}')
        hist = sns.histplot(data = df, x="Mobile_Broadband_Adoption", bins=80, color='navy',alpha = .6,kde=True)
        hist.set_xlabel(r"Mobile Broadband Adoption in %")
        hist.set_ylabel(r"Number of Neighborhoods")


    plt.grid()
    plt.show()

def line(df):
    #set attributes of matplotlib for styling
    #plt.figure(figsize=(14,8))
    sns.set(rc = {'figure.figsize':(15,8)})
    sns.set_theme(style="white")
    #sns.set(style="ticks")
    sns.lmplot(data = df, x="Specialized Enrollment",y="Home_Broadband_Adoption")
    sns.lmplot(data = df, x="Specialized Enrollment",y="Mobile_Broadband_Adoption")
    #plt.title("Mobile Broadband Adoption on Specialized Enrollment")
    plt.title("Home Broadband Adoption on Specialized Enrollment")

    plt.grid()
    plt.show()

def chloropeth(df,type):
    #Open the .geojson file and load the json into nycmap
    nycmap = json.load(open("2010 Neighborhood Tabulation Areas (NTAs).geojson"))
    d = {}
    neighborhood = nycmap["features"]
    #for each neighborhood, sets their nta code
    for n in neighborhood:
        code = n["properties"]["ntacode"]
        a = area(n["geometry"])/(1609*1609) # converts from square meters to square miles
        d[code] = a

    df["area"] = df["NTA_CODE"].map(d)
    df = df.dropna(subset=["area"])
    if (type == "home"):
        fig = px.choropleth_mapbox(df,geojson=nycmap,locations="NTA_CODE",
            featureidkey="properties.ntacode",color="Home_Broadband_Adoption",
            color_continuous_scale="teal",mapbox_style="carto-positron",
            title="Home Broadband Adoption Choropleth", 
            zoom=10, center={"lat": 40.7, "lon": -73.9},opacity=0.8,hover_name="NTA_NAME")
        fig.show()
        fig.write_html(r"C:\Users\chick\Desktop\test\choropleth_home1.html")

    if (type == "mobile"):
        fig = px.choropleth_mapbox(df,geojson=nycmap,locations="NTA_CODE",
            featureidkey="properties.ntacode",color="Mobile_Broadband_Adoption",
            color_continuous_scale="teal",mapbox_style="carto-positron",zoom=9,
            title="Mobile Broadband Adoption Choropleth", 
            center={"lat": 40.7, "lon": -73.9},opacity=0.7,hover_name="NTA_NAME")
        fig.show()
        fig.write_html(r"C:\Users\chick\Desktop\test\choropleth_mobile1.html")
    
    if (type == "providers_available"):
        fig = px.choropleth_mapbox(df,geojson=nycmap,locations="NTA_CODE",
            featureidkey="properties.ntacode",color="Residential Broadband Choice Average by NTA",
            color_continuous_scale="teal",mapbox_style="carto-positron",zoom=9,
            title="Residential Broadband Choices", 
            center={"lat": 40.7, "lon": -73.9},opacity=0.7,hover_name="NTA_NAME")
        fig.show()
        fig.write_html(r"C:\Users\chick\Desktop\test\choropleth_residential_choices1.html")
         

def polynomial(df):
    #Get our independent variables
    cols = ['Home_Broadband_Adoption', 'Specialized Enrollment']
    df = df [cols]
    
    #Create our transformer using scklearn
    transformer = PolynomialFeatures(degree=2)
    X = transformer.fit_transform(df[['Home_Broadband_Adoption']])
    print(X)

    #fit our linear model to the data 
    clf = LinearRegression(fit_intercept=False)
    clf.fit(X, df['Specialized Enrollment'])

    #compare the model to our original data
    sns.lmplot(x='Home_Broadband_Adoption', y='Specialized Enrollment', data=df, fit_reg=False, scatter_kws={'alpha':0.7, 'color':'grey', } )
    xs = np.linspace(.5, 1, 50).reshape(-1, 1)
    ys = clf.predict(transformer.transform(xs))
    plt.plot(xs, ys, color ='black')
    plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    plt.title('Degree 2 polynomial fit')



    plt.show()

def multiple_linear(df):
    #get our independent and dependent variables
    x = df[['Mobile_Broadband_Adoption', 'Home_Broadband_Adoption']]
    y = df['Specialized Enrollment']

    #split our training cases and test cases
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.4)
    linreg = LinearRegression()
    #fit our model
    linreg.fit(x_train,y_train)
    x3d = x_test['Home_Broadband_Adoption']
    y3d = x_test['Mobile_Broadband_Adoption']
    z3d = linreg.predict(x_test)

    #create our line
    coords = np.array((x3d, y3d, z3d)).T
    print(coords)
    pca = PCA(n_components=1)
    pca.fit(coords)
    vect = pca.components_
    origin = np.mean(coords, axis=0)
    euclidian_distance = np.linalg.norm(coords - origin, axis=1)
    extent = np.max(euclidian_distance)
    line = np.vstack((origin - vect * extent, origin + vect * extent))

    #create our 3d scatter plot with multiple linear regression
    ax = plt.axes(projection='3d')
    ax.scatter3D(x3d, y3d, z3d, marker='x', cmap='Greens')
    ax.plot3D(line[:, 0], line[:, 1], line[:, 2], 'gray')
    ax.set_xlabel('Home Broadband Adoption')
    ax.set_ylabel('Mobile Broadband Adoption')
    ax.set_zlabel('Specialized High School Enrollment')
    plt.title('Multiple Linear Regression of Mobile and Home broadband adoption to Specialized High School Enrollment')
    plt.show()

internet_df = make_internet_df("Internet_Master_Plan__Adoption_and_Infrastructure_Data_by_Neighborhood.csv", )
school_shsat_df = make_school_df("2017-2018_SHSAT_Admissions_Test_Offers_By_Sending_School.csv", "2017_-_2018_School_Locations.csv")
df = combine_df(internet_df,school_shsat_df)

#histogram(internet_df,"mobile")
#line(df)
#chloropeth(internet_df,"providers_available")
#polynomial(df)
#multiple_linear(df)
