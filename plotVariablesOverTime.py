import RAD_Sanitation as RADS
import countryList as RADCL
import pickle
import matplotlib.pyplot as plt
import pprint
import numpy as np
import pylab
import scipy.stats
import matplotlib as mpl

plt.rcParams["figure.figsize"] =[12,12]

data_values = {'% Gross Female Secondary School Enrollment': "dataPickles/grossSecondarySchoolEnrolment.p",
	'Improved Water Source (% access)':"dataPickles/improvedWaterSource.p",
	'Improved Sanitation Facilities (% access)':"dataPickles/ImprovedSan.p",
	'% Access to Contraceptives': "dataPickles/contraceptivePrevalance.p",
	'Lower Secondary Schools With Toilets (%)': "dataPickles/unesco_Percentage of lower secondary schools with toilets (%).p",
	'Percentage of Primary Schools Without Toilets (%)':"dataPickles/unesco_Percentage of primary schools without toilets (%).p",
	'Percentage of Primary Schools with Toilets (%)':"dataPickles/unesco_Percentage of primary schools with toilets (%).p",
	'Percentage of Primary Schools with Mixed-Sex Toilets (%)':"dataPickles/unesco_Percentage of primary schools with mixed-sex toilets (%).p",
	'Percentage of Lower Secondary Schools with Single-Sex Toilets (%)':"dataPickles/unesco_Percentage of lower secondary schools with single-sex toilets (%).p",
	'Correct gross fem secondary school enrollemnt':'dataPickles/% Gross Female Secondary School Enrollment-C.p'
}


little_plots = True # :Plot the little plots of the scatter data with different time offsets
axies_scale = 'linear' # :Plot nad compute the values with log/log axies. Options include: 'log_log'

variable_name_plot_dependent = 'Percentage of Lower Secondary Schools with Single-Sex Toilets (%)'#'Improved Sanitation Facilities (% access)'#
variable_name_plot_independent = '% Gross Female Secondary School Enrollment'#'% Gross Female Secondary School Enrollment'

#[(Country, indicator, [values],[years]), (Country, indicator, [values],[years]),...]


dependent = pickle.load( open( data_values[variable_name_plot_dependent], "rb" ) )
independent = pickle.load( open( data_values[variable_name_plot_independent], "rb" ) )

pprint.pprint(independent)


country_list = ['Angola',
	'Benin',
	'Botswana',
	'Burkina Faso',
	'Burundi',
	'Cameroon',
	'Central African Republic',
	'Chad',
	'Comoros',
	'Djibouti',
	'Equatorial Guinea',
	'Eritrea',
	'Ethiopia',
	'Gabon',
	'Ghana',
	'Guinea',
	'Guinea-Bissau',
	'Kenya',
	'Lesotho',
	'Liberia',
	'Madagascar',
	'Malawi',
	'Mali',
	'Mauritania',
	'Mauritius',
	'Mozambique',
	'Namibia',
	'Niger',
	'Rwanda',
	'Sao Tome and Principe',
	'Senegal',
	'Seychelles',
	'Sierra Leone',
	'Somalia',
	'South Africa',
	'Sudan',
	#'Swaziland',
	#'Tanzania',
	#'Togo',
	'Uganda',
	'Zambia',
	'Zimbabwe']

def generate_list_of_Countries(data_list):
    countryList = []
    
    for data in data_list:
        countryList.append( data[0] )
        
    return countryList
        

dependent = RADS.ourCountries(dependent, country_list)
independent = RADS.ourCountries(independent, country_list)


## Re-order the countries in the dependent caraible to the order of the independent variable:
dependent_new=[]
for country_set in independent:
    country = country_set[0]
    for country_set_dependent in dependent:
        if country_set_dependent[0] == country:
            dependent_new.append(country_set_dependent)
dependent = dependent_new

## Get a list of countries present in each data set:
dependent_country_list = generate_list_of_Countries(dependent)
independent_country_list = generate_list_of_Countries(independent)

## Exclude any country that isn't included in the other data set
mutualCountries = []
for country_set in independent:
    country = country_set[0]
    if (country in dependent_country_list):
        mutualCountries.append(country_set)
independent = mutualCountries

## Do above exclusion for the other data set:
mutualCountries = []
for country_set in dependent:
    country = country_set[0]
    if (country in independent_country_list):
        mutualCountries.append(country_set)
dependent = mutualCountries



###def crossCorrelateValuesForPlotting(data1, data2, country, yearOffset=0):
###    for 
###	d1,d2,years = RADS.yearCorrelate(data1, data2[countryIndex], yearOffset = yearOffset)

###	d1 = np.array(d1); d2=np.array(d2)
###	if (len(d1)>1) and (len(d2)>1):
###		return d1, d2
###	else:
###		#print 'Country ', countryIndex, ' has no data for given indicator.'
###		return d1, d2

## Make color map for unique colors per country: 
## Color map documentation & options here: 
## http://matplotlib.org/examples/color/colormaps_reference.html
## Set1 works well
colorArray = mpl.cm.hsv( np.linspace(0,1,len(country_list)) )


d1_all = []; d2_all = []
for country in country_list:
    #print 'Country is: ', country
    #d1, d2 = crossCorrelateValuesForPlotting(dependent, independent, country_index)
    depSet=False
    indSet=False
    for valueSet in dependent:
        if valueSet[0] == country:
            depSet = valueSet
    for valueSet in independent:
        if valueSet[0]==country:
            indSet = valueSet
    if (depSet!=False) and (indSet!=False):
        d1, d2, years = RADS.yearCorrelate(depSet, indSet, 0)
        d1 = np.array(d1)
        d2 = np.array(d2)
        m, b, r_value, p_value, std_err = scipy.stats.linregress(d1,d2)
        
        
        if  (len(d1)>1):
            currentLenD1 = len(d1)
            d1_all.append(d1); d2_all.append(d2)
            plt.plot(d1,d2, 
                marker='h', 
                ls='.', 
                markersize=15, 
                color = colorArray[country_list.index(country)], 
                alpha=.99, 
                label = country  )
    #        print country_values[0]
    #        print country_values
                
            plt.plot(d1, d1*m + b, color = colorArray[country_list.index(country)], linewidth=3, linestyle=':')
    #        print country_values[0], 'has data'
    #        if country_values[0] == 'Benin':
    #            print d1
    #            print d2
#    else:
#        print country_values[0], 'has no data'
#        print d1[0]
#        try:
#            if d1[0]<50:
#                print '\nproblem child:   ', country_values, zip(d1,d2)
#        except:
#            print '\nevil child:   ', country_values
#            print 'd1: ', d1, ' d2: ', d2
#            print len(d1), currentLenD1
#        if d2[0]>30:
#            print '\ntall one: ', country_values, zip(d1,d2)


d1_log = []
d2_log = []	

d1_values = []
d2_vlaues = []

for array in d1_all:
	for nested_value in array:
		d1_log.append(np.log10(nested_value))
		d1_values.append(nested_value)

for array in d2_all:
	for nested_value in array:
		d2_log.append(np.log10(nested_value))
		d2_vlaues.append(nested_value)

# pprint.pprint(d2_log)
d1_log = np.array(d1_log)
d2_log = np.array(d2_log)
d1_values = np.array(d1_values)
d2_vlaues = np.array(d2_vlaues)


# line, = ax.plot(d1, m*d1+b, marker = 'o', color='red', lw=8)#plt.plot(d1,m*d1+b, linewidth=8)
if axies_scale=='log_log':
	x = d1_log
	y = d2_log
if axies_scale=='linear':
	x=d1_values
	y=d2_vlaues
m, b, r_value, p_value, std_err = scipy.stats.linregress(x, y)
pearsonCorrelation = scipy.stats.pearsonr(x, y)	
print 'r squared: ', r_value**2
print 'p val: ', p_value
print 'standard error: ', std_err
print 'line slope: ', m
print 'line intercept: ', b
print 'Pearson correlation: ', pearsonCorrelation
print '\n'


#plt.clf()
#plt.plot(x, y, 'o', markersize=13, alpha=.5)
plt.plot(x, m*x+b, linewidth=5, color='purple', label='Overall OLS Line')
# plt.show()
plt.ylabel(variable_name_plot_independent, fontsize=18)
plt.xlabel(variable_name_plot_dependent, fontsize=18)
plt.suptitle('Effect of '+variable_name_plot_dependent+' \n on '+variable_name_plot_independent, fontsize=20)
subtitle = '$R^2$ value of: '+str(r_value**2) + ', $P$ value of: '+str(p_value)
plt.title(subtitle, fontsize=13)

#Make a pretty legend. Documentation here: http://matplotlib.org/api/legend_api.html
plt.legend(fontsize=10, loc=2, ncol=2) 

# plt.plot(independent[1][3],independent[1][2], linewidth=8)

plt.show()
#plt.savefig(variable_name_plot_dependent+'_offsetScatterPlot_offsetOf'+str(yearOffset)+'.png', papertype='letter')
		
	
