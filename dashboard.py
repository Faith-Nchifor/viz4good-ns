import pandas as pd

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# dataframe = pd.read_csv('ns_data.csv')
if 'time' not in st.session_state:
    st.session_state.time = None

if 'df' not in st.session_state:
    st.session_state.df = pd.read_csv('ns_data.csv')

if 'selected_age' not in st.session_state:
    st.session_state.selected_age = None
if 'selected_postcode' not in st.session_state:
    st.session_state.selected_postcode = None

df = st.session_state.df


df_static = pd.read_csv('ns_data.csv')

percentage_teens= round((df_static[(df_static['start_age']>12) & (df_static['start_age']<18)].shape[0]/df_static.shape[0] ) * 100,2)

postcodes = [name for name in df_static['code_name'].unique()]

age_grps = df_static.groupby('start_age')
mean_score_age = pd.DataFrame({
    'group':list(age_grps.groups.keys()),
    'pop_count':[len(x) for x in list(age_grps.groups.values())],
    'mean_start_score':age_grps['start_score'].mean(),
    'mean_end_score':age_grps['end_score'].mean(),
   
})
mean_score_age['points']=mean_score_age['mean_end_score'] - mean_score_age['mean_start_score']

# score by industry
mean_score_indus = df.groupby('industry')
mean_pt_score_indus = pd.DataFrame({
     'industry': mean_score_indus['start_score'].mean().index,
    'mean_start_score': mean_score_indus['start_score'].mean().values,
     'mean_end_score': mean_score_indus['end_score'].mean().values,
    
})
mean_pt_score_indus['points'] =mean_pt_score_indus['mean_end_score'] - mean_pt_score_indus['mean_start_score']

#define gender scores
data_gender_melted =  pd.melt(df, id_vars=['gender'], value_vars=['start_score', 'end_score'],
                      var_name='score_type', value_name='score')

df_copied = df.copy()
data_shape = st.session_state.df.shape
def on_change_callback():
    age = st.session_state.selected_age
    postcode = st.session_state.selected_postcode
    cur= df_static
    if (age):
        # cur= st.session_state.df
        cur = cur[cur['start_age']==age]
        # st.session_state.df = cur
    if(postcode):
        cur = cur[cur['code_name']==postcode]

    st.session_state.df = cur

def clear_fields():
       st.session_state.selected_age =None
       st.session_state.selected_postcode = None
       st.session_state.df = df_static
        
    
   
def visualize():
    # sns.choose_colorbrewer_palette()
    st.image('./VFSG Logo to include on viz - light background(1).png')
    sns.color_palette(palette='BuPu')
    st.title('Visualizing the Impact of Noise solution')
    st.write('Noise solution(NS) began its work in 2021 and has seen persons from over 400 indiduals from 18  postcode areas. using it\'s method of Self expression through \
            Music there has been an overall improvement in the mental welbeing most of the participants of this program. The participants mental wellbeing is measured according to SWEMWBS scale.\
            The improvement is visible accross ages, industries of reference, gender, and postcode areas')

    #
    st.write(f"The average end score is  {round(df_static['end_score'].mean(),2)} which is an overall 'Moderate' when measured against the national averages for 'high', 'moderate', and 'low' as described in 'SWEMWBS Population Norms in Health Survey for England data 2011'")

    fig = plt.figure(figsize=(12, 4))
    sns.histplot(x = "end_score",  data = df_static,kde=True,color='#8755ff')
    plt.xticks(rotation=45)
    plt.title('Distribution of end scores')
    plt.ylabel('frequency')
    plt.xlabel('Score')
    
    st.pyplot(fig)


    st.header('Impact by age')
    st.write('The SWEMWBS scale has been validated for populations of young people (15 - 21) and the general population. According to NS, the minimum age of participants \
            is 8 and the max age is 60. ')
    st.write(f'{percentage_teens} of participants were between the ages of 13 and 17')
    fig = plt.figure(figsize=(12, 4))
    sns.countplot(x = "start_age",  data = df_static,color='#01070A')
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_formatter(PercentFormatter(df_static.shape[0]))
    plt.title('Distribution of participant Ages')
    plt.ylabel('%')
    plt.xlabel('Age')
    # plt.xticks(ticks=[5,10,15,20,25,30,35,40,45,50,55,60])
    st.pyplot(fig)


    st.write('The points - the difference between the start and end score ')
   
    col1, col2 = st.columns(2)

    # with col1:
    #     st.subheader("start scores")
    #     fig = plt.figure(figsize=(12, 4))
    #     # sns.lineplot(data=mean_score_age, x='group',y='points',label='points')
    #     sns.lineplot(data=mean_score_age, x='group',y='mean_end_score',label='end score')
    #     sns.lineplot(data=mean_score_age, x='group',y='mean_start_score',label='start score')
    #     plt.title('points gotten by age')
    #     plt.xlabel('Age')
        
    #     plt.grid()
    #     st.pyplot(fig)
    st.header('Assessment of result by points')
    st.write('Points refer to the changes in scores at the end of the program. They are obtained by subtracting the start score from the end score. A point greater than zero indicates a positive improvement and vice versa. In the following plots, we see the improvement of individuals across gender, industry of reference, age and postcode')

    # with col2:
    st.subheader("Average points by age")
    # st.write('points are the differences between start and end scores')
    
    fig = plt.figure(figsize=(12, 4))
    sns.lineplot(data=mean_score_age, x='group',y='points',label='points')
    
    plt.title('Average points  by age')
    plt.xlabel('Age')
    plt.xticks(list(range(0,61,5)))
    plt.grid()
    st.pyplot(fig)

    st.write('In the following sections, You can interact with the plots that follow by changing the age and post code')
    colA,colB,colC = st.columns(3)
    with colA:

        st.selectbox('select age',list(df_static['start_age'].unique()),key='selected_age')
    with colB:
        st.selectbox('Postcode',postcodes,key='selected_postcode') 
    with colC:
        # st.selectbox('select year',list(df_static['year'].unique()),on_change=on_change_callback,key='selected_year')
        st.button('Search',on_click=on_change_callback)
        if((st.session_state.selected_age is not None) | (st.session_state.selected_postcode is not None)):
            st.button('clear filter',on_click=clear_fields)
    col1,col2,col3 = st.columns(3)
    with col1:
        st.write(f'Selected Age :{st.session_state.selected_age}')
    with col2:
        st.write(f'Selected Postcode :{st.session_state.selected_postcode}')
    with col3:
        st.write(f'length of result :{st.session_state.df.shape[0]}')

    st.header('Impact by industry')
    st.write('There are a total of 3 nambed industries.')

    col1,col2 = st.columns(2)

    with col1:
        fig = plt.figure(figsize=(12, 4))
        sns.countplot(x=df['industry'])
        plt.title('distributions of industries ')
        plt.ylabel('')
        st.pyplot(fig)
    with col2:
        st.dataframe(mean_pt_score_indus,use_container_width=True)
        st.write('Individuals refered from mental health industry benefited the most from this program given they have the highest points')
    st.header('By gender')
    st.write('Gender information had some missing values. However, we see that the male gender is the dominant of all genders ')
    fig = plt.figure(figsize=(12, 4))
    sns.countplot(x=df['gender'])
    plt.title('distribution of gender of participants')
    plt.xticks(rotation=45)
    st.pyplot(fig)
   
    st.write('We also see a significant improvement amongsth participants who identified themselves')
    fig = plt.figure(figsize=(12, 4))
    sns.barplot(data=data_gender_melted, x='gender', y='score', hue='score_type', errorbar=None)
    plt.title('Average Start and End Scores by Gender')
    st.pyplot(fig)

    
    

if __name__ == '__main__':
    visualize()
