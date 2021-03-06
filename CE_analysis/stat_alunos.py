"""
stat_2016_alunos.py
Descriptive and inferential statistics in Python.
Use numpy, scipy and matplotlib.
"""
__author__ = 'Ernesto Costa'
__date__ = 'March 2015, March 2016'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

# obtain data
def get_data(filename):
    data = np.loadtxt(filename)
    return data

def get_data_many(filename):
    data_raw = np.loadtxt(filename)
    data = data_raw.transpose()
    #print(data)
    return data

# describing data

def describe_data(data):
    """ data is a numpy array of values"""
    min_ = np.amin(data)
    max_ = np.amax(data)
    mean_ = np.mean(data)
    median_ = np.median(data)
    mode_ = st.mode(data)
    std_ = np.std(data)
    var_ = np.var(data)
    skew_ = st.skew(data)
    kurtosis_ = st.kurtosis(data)
    q_25, q_50, q_75 = np.percentile(data, [25,50,75])
    basic = 'Min: %s\nMax: %s\nMean: %s\nMedian: %s\nMode: %s\nVar: %s\nStd: %s'
    other = '\nSkew: %s\nKurtosis: %s\nQ25: %s\nQ50: %s\nQ75: %s'
    all_ = basic + other
    print(all_ % (min_,max_,mean_,median_,mode_,var_,std_,skew_,kurtosis_,q_25,q_50,q_75))
    return (min_,max_,mean_,median_,mode_,var_,std_,skew_,kurtosis_,q_25,q_50,q_75)

# visualizing data
def histogram(data,title,xlabel,ylabel,bins=25):
    plt.hist(data,bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    
def histogram_norm(data,title,xlabel,ylabel,bins=20):
    plt.hist(data,normed=1,bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    min_,max_,mean_,median_,mode_,var_,std_,*X = describe_data(data)
    x = np.linspace(min_,max_,1000)
    pdf = st.norm.pdf(x,mean_,std_)
    plt.plot(x,pdf,'r')    
    plt.show()

def box_plot(data, labels):
    plt.boxplot(data,labels=labels)
    plt.xticks(rotation=90)
    #plt.xticks()
    plt.show()


# Parametric??
def test_normal_ks(data):
    """Kolgomorov-Smirnov"""
    norm_data = (data - np.mean(data))/(np.std(data)/np.sqrt(len(data)))
    return st.kstest(norm_data,'norm')

def test_normal_sw(data):
    """Shapiro-Wilk"""
    norm_data = (data - np.mean(data))/(np.std(data)/np.sqrt(len(data)))
    return st.shapiro(norm_data)

def levene(data):
    """Test of equal variance."""
    W,pval = st.levene(*data)
    return(W,pval)

# hypothesis testing
# Parametric
def t_test_ind(data1,data2, eq_var=True):
    """
    parametric
    two samples
    independent
    """
    t,pval = st.ttest_ind(data1,data2, equal_var=eq_var)
    return (t,pval)

def t_test_dep(data1,data2):
    """
    parametric
    two samples
    dependent
    """
    t,pval = st.ttest_rel(data1,data2)
    return (t,pval)

def one_way_ind_anova(data):
    """
    parametric
    many samples
    independent
    """
    F,pval = st.f_oneway(*data)
    return (F,pval)

def one_way_dep_anova(data_frame):
    """
    parametric
    many samples
    independent
    @data_frame: a  pandas DataFrame with the data
    """
    grand_mean = data_frame.mean()
    #grand_variance = data_frame.values.var(ddof=1)
    
    row_means = data_frame.mean(axis=1)
    column_means = data_frame.mean(axis=0)
    
    # n = number of subjects; k = number of conditions/treatments
    n,k = len(data_frame.axes[0]), len(data_frame.axes[1])
    # total number of measurements
    N = data_frame.size # or n * k
    
    # degrees of freedom
    df_total = N - 1
    df_between = k - 1
    df_subject = n - 1
    df_within = df_total - df_between
    df_error = df_within - df_subject   
       
    # compute variances
    SS_between = sum(n*[(m - grand_mean)**2 for m in column_means])   
    SS_within = sum(sum([(data_frame[col] - column_means[i])**2 for i,col in enumerate(data_frame)]))  
    SS_subject = sum(k* [(m - grand_mean)**2 for m in row_means])  
    SS_error = SS_within - SS_subject  
    #SS_total = SS_between + SS_within
    
    # Compute Averages
    MS_between = SS_between/df_between
    MS_error = SS_error/df_error
    MS_subject = SS_subject/df_subject
    
    # F Statistics
    F = MS_between/MS_error
    # p-value
    p_value = st.f.sf(F,df_between,df_error)   
    
    return (F, p_value)

# Non Parametric
def mann_whitney(data1,data2):
    """
    non parametric
    two samples
    independent
    """    
    return st.mannwhitneyu(data1, data2)

def wilcoxon(data1,data2):
    """
    non parametric
    two samples
    dependent
    """     
    return st.wilcoxon(data1,data2)

def kruskal_wallis(data):
    """
    non parametric
    many samples
    independent
    """     
    H,pval = st.kruskal(*data)
    return (H,pval)

def friedman_chi(data):
    """
    non parametric
    many samples
    dependent
    """     
    F,pval = st.friedmanchisquare(*data)
    return (F,pval)    
    
# Effect size
def effect_size_t(stat,df):
    r = np.sqrt(stat**2/(stat**2 + df))
    return r

def effect_size_mw(stat,n1,n2):
    """
    n_ob: number of observations
    """
    n_ob = n1 + n2 
    mean = n1*n2/2
    std = np.sqrt(n1*n2*(n1+n2+1)/12)
    z_score = (stat - mean)/std
    print(z_score)
    return z_score/np.sqrt(n_ob)

def effect_size_wx(stat,n, n_ob):
    """
    n: size of effective sample (zero differences are excluded!)
    n_ob: number of observations
    """
    mean = n*(n+1)/4
    std = np.sqrt(n*(n+1)*(2*n+1)/24)
    z_score = (stat - mean)/std
    return z_score/np.sqrt(n_ob)

# To test the methods

def main_1():
    # Pulse Rate example (one group)
    pr = get_data(prefix+'pulse_rate.txt')
    describe_data(pr)
    print(test_normal_ks(pr))    
    histogram(pr, 'Histogram','Pulse Rate', 'Frequency')
    
def main_11():
    # Pulse Rate example (one group)
    pr = get_data(prefix+'pulse_rate.txt')
    box_plot(pr,['PR'])

     
    
def main_111():
    # Pulse Rate example (one group)
    pr = get_data(prefix+'pulse_rate.txt')
    describe_data(pr)
    print(test_normal_ks(pr))    
    histogram_norm(pr, 'Histogram','Pulse Rate', 'Frequency')  
    
    
    
def main_3():
    # Spider example (2 groups)
    sp = get_data_many(prefix+'spider.txt')
    fake_sp = sp[0,:]
    real_sp = sp[1,:]
    t,pval = t_test_dep(fake_sp,real_sp)
    print('t: %s   p_value: %s' % (t,pval))
    r = effect_size_t(t,len(fake_sp)-1)
    print('Effect size:  %s' % r)
    
    min_ = min([np.amin(sp[i,:]) for i in range(len(sp))])
    max_ = max([np.amax(sp[i,:]) for i in range(len(sp))])    
    plt.axis(ymin=min_ - 20, ymax=max_ + 20)
    plt.title('Anxiety to spiders')
    plt.ylabel('Level')
    
    box_plot([fake_sp,real_sp],['Fake','Real'])


def main_31():
    # Spider example (2 groups)
    sp = get_data_many(prefix+'spider.txt')
    fake_sp = sp[0,:]
    real_sp = sp[1,:]
    t,pval = t_test_dep(fake_sp,real_sp)
    print('t: %s   p_value: %s' % (t,pval))
    r = effect_size_t(t,len(fake_sp)-1)
    print('Effect size:  %s' % r)
   
    histogram(fake_sp, 'Anxiety to spiders','Level','Value' )


def main_311():
    # Spider example (2 groups)
    sp = get_data_many(prefix+'spider.txt')
    fake_sp = sp[0,:]
    real_sp = sp[1,:]
    u, p = mann_whitney(fake_sp,real_sp)
    print('u= %f   p = %s' % (u, p))
    t,p = t_test_ind(fake_sp,real_sp)
    print('t= %f   p = %s' % (u, p))

       
    
if __name__ == '__main__':
    # The following variable should be edited by you
    prefix='/Users/ernestojfcosta/tmp/'
    #main_1()
    #main_11()
    #main_111()
    #main_3()
    #main_31()
    main_311()
       
    
    """
    # Spider example (2 groups)
    sp = get_data_many(prefix+'spider.txt')
    fake_sp = sp[0,:]
    real_sp = sp[1,:]
    t,pval = t_test_dep(fake_sp,real_sp)
    print(t,pval)
    r = effect_size_t(t,len(fake_sp)-1)
    print(r)
    #min_ = min([np.amin(sp[i,:]) for i in range(len(sp))])
    #max_ = max([np.amax(sp[i,:]) for i in range(len(sp))])    
    #plt.axis(ymin=min_ - 20, ymax=max_ + 20)new_arr
    #plt.title('Anxiety to spiders')
    #plt.ylabel('Level')
    #box_plot(pr,['PR'])
    #box_plot([fake_sp,real_sp],['Fake','Real'])
    #plt.title('Ansiety: fake spider')
    #histogram(fake_sp)
    #spy = get_data_two(prefix+'spider.txt')
    #print(mann_whitney(spy[0,:],spy[1,:]))
    #print(t_test_ind(fake_sp,real_sp))
    #print(t_test_dep(fake_sp,real_sp))    
    

    
    # Sphere example (3 groups)
    #sphere = get_data_many(prefix+'sphere_3.txt')
    #print(kruskal_wallis(sphere))
    #print(friedman_chi(sphere))
    #print(levene(sphere))    
    #print(one_way_ind_anova(sphere))

    # Effect size
    print(effect_size_t(t,len(fake_sp)-1))
    print(effect_size_mw(35.5,10,10))
    print(effect_size_wx(0,8,20))
    """