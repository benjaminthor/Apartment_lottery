# import libraries for project
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# set up Streamlit layout to full screen 
st.set_page_config(layout="wide")

# read processed Data frame
df = pd.read_csv('with_region.csv')
df['Last Date Registration'] = pd.to_datetime(df['Last Date Registration'])
# Hebrew words needs to revers so it will be presented in the write order    
df['reversed_locations'] = df['Location'].apply(lambda x: x[::-1])
# Create a dictionary to store the frequency of each location
location_freq = df['reversed_locations'].value_counts().to_dict()

############################### Word Cloud plot based on frequency of lotteries ################################
wordcloud = WordCloud(width=1200, height=600, background_color='white', font_path='arial-hebrew.ttf').generate_from_frequencies(location_freq)

st.markdown("<h1 style='text-align: center; color: black;'>פרוייקט קורס - הדמיית נתונים- מחיר למשתכן</h1>", unsafe_allow_html=True)
st.image(wordcloud.to_array(), use_column_width=True)

############################## Explore data with - Data Frame Top 5 display #######################
st.write("""
<style>
    .rtl {
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)
st.write("<div class='rtl'>5 שורות ראשונות מהטבלה</div>", unsafe_allow_html=True)

st.write(df.drop(columns='reversed_locations').head(5))


################################ Tree plot ######################################
tree_df = pd.DataFrame(df.groupby(['Location','Region','country']).agg({'Price per Meter':'mean',
                                                   'Lottery Number':'size',
                                                   'Natives Chance to win':'mean',
                                                   'non-Natives Chance to win':'mean', 
                                                   'Registered':'sum'})).reset_index()#name=['Price per Meter_mean','Lottery Number_count','Natives Chance to win_mean','non-Natives Chance to win_mean'])
tree_df.columns = [
    'Location',
    'Region',
    'country',
    'Mean Price per Meter',
    'Number of Lotteries',
    'Natives Mean Chance to win',
    'Mean Chance to win',
    'מספר נרשמים כולל'
]
# Create a TreeMap
fig = px.treemap(tree_df, path=['country','Region','Location'], 
                  values='Number of Lotteries', 
                    color='מספר נרשמים כולל',
                 hover_data=['Mean Price per Meter',
                            'Number of Lotteries',
                            'Natives Mean Chance to win',
                            'Mean Chance to win',
                            'מספר נרשמים כולל'],
                 color_continuous_scale='RdBu', 
                 hover_name='Location',
                 width=1300, height=800
                 )

# Format hover template to display three numbers after the decimal point
fig.update_traces(marker=dict(cornerradius=5),
    hovertemplate='<b>מיקום:</b> %{label}<br>' +
                                '<b>מחיר ממוצע למטר:</b> %{customdata[0]:.2f}<br>' +
                                '<b>מספר הגרלות:</b> %{customdata[1]:.0f}<br>' +
                                '<b>סיכוי ממוצע לזכיה עבור בן מקום:</b> %{customdata[2]:.3f}<br>' +
                                '<b>ממוצע לזכיה כללי:</b> %{customdata[3]:.3f}<br><extra></extra>'+
                                '<b>מספר נרשמים כולל:</b> %{customdata[4]}<br>'
                                )
# fig2.update_layout(font=dict(size=15), title_x=0.5, title_y=0.95)

st.markdown("<h3 style='text-align: center; color: black;'>מידע על הגרלות על בסיס מיקום</h3>", unsafe_allow_html=True)

st.plotly_chart(fig, use_container_width=True)
################################# Sankey plot #########################################
m_df = pd.read_excel('mishtaken_data.xlsx')
# Assuming data is your DataFrame containing the data
data = m_df.groupby(['ConstructionPermitName', 'ProjectStatus']).size().reset_index(name='value_count')
data.drop(0,inplace=True)
# Get unique node labels
labels = pd.concat([data['ConstructionPermitName'], data['ProjectStatus']]).unique()

# Create a mapping from labels to indices
label_to_index = {label: idx for idx, label in enumerate(labels)}

# Create source and target indices for the Sankey plot
source_indices = data['ConstructionPermitName'].map(label_to_index)
target_indices = data['ProjectStatus'].map(label_to_index)

# Create a Sankey plot using Plotly graph objects
fig1 = go.Figure(data=[go.Sankey(
    node=dict(
        pad=10,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=data['value_count'],
        color='rgba(0, 0, 255, 0.2)' 
    )
    
)])

# Update layout and show plot
# fig1.update_layout(
#  xaxis=dict(title_text="X Axis Title"),
#     yaxis=dict(title_text="Y Axis Title")
#                    )

st.markdown("<h3 style='text-align: center; color: black;'>מצב הפרוייקט אל מול מצב אישור הבנייה - מרבית הדירות בהיתר מלא נבחרו</h3>", unsafe_allow_html=True)

st.plotly_chart(fig1, use_container_width=True)

############################## Numeric features - Correlation Matrix plot #######################

correlation_matrix = df.loc[:,['Number of Apartments', 'Apartments for Natives', 'Registered','Registered Natives', 'Price per Meter']].corr()
heatmap = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5,vmin=-1, vmax=1)
plt.xticks(rotation=45,fontsize=6)
plt.yticks(fontsize=6)
cbar = heatmap.collections[0].colorbar
cbar.ax.tick_params(labelsize=6)

st.markdown("<h3 style='text-align: center; color: black;'>מטריצת קורלציה: המחיר אינו משפיע על ההגרלה</h3>", unsafe_allow_html=True)
st.pyplot(plt)

############################## Rasing trend yearly number of lotteries - Time series plot  #######################

# Group by date and calculate the event count for each date
reg_df = df.groupby('Last Date Registration').size().reset_index(name='event_count')

# Group by year and calculate the mean event count for each year
reg_df['Year'] = reg_df['Last Date Registration'].dt.year
mean_event_count = reg_df.groupby('Year')['event_count'].mean().reset_index()

# Create Plotly figure
fig = go.Figure()

# Add trace for event count
fig.add_trace(go.Scatter(x=reg_df['Last Date Registration'], y=reg_df['event_count'],
                    mode='lines+markers', name='מספר הגרלות'))

# Add trace for mean event count
fig.add_trace(go.Scatter(x=mean_event_count['Year'], y=mean_event_count['event_count'],
                    mode='lines+markers', name='ממוצע שנתי של מספר ההגרלות'))

# Update figure layout
fig.update_layout(
                  xaxis=dict(title='תאריך' ,titlefont=dict(size=20),showgrid=True),
                  yaxis=dict(title='מספר הגרלות',titlefont=dict(size=20)),
                  legend=dict(x=0, y=1, traceorder="normal"),width=1300, height=800)

st.markdown("<h3 style='text-align: center; color: black;'>מגמה עולה במספר ההגרלות</h3>", unsafe_allow_html=True)
# Display Plotly figure in Streamlit
st.plotly_chart(fig, use_container_width=True)

############################### Region based count - time series plot ##########################

# Group by date and region and calculate the count
lottery_count_by_date_region = df.groupby(['Last Date Registration', 'Region']).size().reset_index(name='LotteryCount')
# lottery_count_by_date_region = lottery_count_by_date_region.replace({'South':'דרום','North':'צפון','Center':'מרכז'})

# Plot the stacked area chart
fig = px.area(lottery_count_by_date_region, x='Last Date Registration', y='LotteryCount', color='Region', 
              labels={'Last Date Registration': 'תאריך', 'LotteryCount': 'מספר הגרלות', 'Region': 'אזור'},
              category_orders={'Region': ['North', 'Center', 'South']},
              width=1300, height=800)
fig.update_layout(
                  xaxis=dict(titlefont=dict(size=20),showgrid=True),
                yaxis=dict(titlefont=dict(size=20)))

st.markdown("<h3 style='text-align: center; color: black;'>יותר הגרלות במרכז</h3>", unsafe_allow_html=True)

st.plotly_chart(fig, use_container_width=True)
#################################### Region based bar plot chance to win #####################

grouped_df = df.groupby(['Region']).agg({'Natives Chance to win':'mean', 
                                         'non-Natives Chance to win':'mean',
                                         'Number of Apartments':'mean',
                                         'Apartments for Natives':'mean'}).reset_index()
# Define the custom sorting order
custom_order = {'צפון': 0, 'מרכז': 1, 'דרום': 2}

# Sort the DataFrame based on the custom sorting order
grouped_df['Region_Order'] = grouped_df['Region'].map(custom_order)
grouped_df = grouped_df.sort_values(by='Region_Order').drop(columns='Region_Order')
grouped_df.rename(columns={'Natives Chance to win':'סיכוי זכייה לבן מקום', 'non-Natives Chance to win':'סיכוי זכייה כללי'},inplace=True)
fig = px.bar(grouped_df, x='Region', y=['סיכוי זכייה לבן מקום', 'סיכוי זכייה כללי'],
             barmode='group',
             hover_data={'Number of Apartments': True, 'Apartments for Natives':True,'Number of Apartments':True},
             labels={ 'variable': 'אוכלוסיה'},
             width=1000, height=700)

fig.update_layout(
                  xaxis=dict(title='אזור',titlefont=dict(size=20)),
                yaxis=dict(title='סיכוי זכייה',titlefont=dict(size=20)))
fig.update_traces(
    hovertemplate='<b>סיכויי זכייה ממוצע:</b> %{value:.2f}<br>' +
                    '<b>מספר דירות מממוצע בפרויקט:</b> %{customdata[0]:.2f}<br>' +
                    '<b>מספר דירות ממוצע לבן מקום:</b> %{customdata[1]:.2f}<br>'
                                )

st.markdown("<h3 style='text-align: center; color: black;'>סיכוי הצלחה גבוהים עבור בן מקום לעומת מי שאינו</h3>", unsafe_allow_html=True)
# Show the plot
st.plotly_chart(fig, use_container_width=True)

################################## Ascending price per meter - Time sires plot ###############################3

st.write("""
<style>
    .rtl {
        direction: rtl;
        text-align: right;
    }
    font-size: 45px;
</style>
""", unsafe_allow_html=True)
st.write("<div class='rtl'><p style='font-size: 25px;'>בחר עד חמישה מיקומים</p></div>", unsafe_allow_html=True)


# Create a multiselect dropdown for selecting locations
selected_locations = st.multiselect('', df['Location'].unique(), default=df['Location'].unique()[:5], key='locations', 
                                    max_selections=5)

# Filter the DataFrame based on selected locations
filtered_df = df[df['Location'].isin(selected_locations)]
# st.write("Sample of 3 rows of the DataFrame:")
grouped_df = filtered_df.groupby(['Location','Last Date Registration'])['Price per Meter'].mean().reset_index()
# st.write(grouped_df.sample(n=3))

# Plot the time series using Plotly
fig = go.Figure()

# Add trace for event count
for location in selected_locations:
    fig.add_trace(go.Scatter(x=grouped_df.loc[grouped_df['Location']==location,'Last Date Registration'], 
                             y=grouped_df.loc[grouped_df['Location']==location,'Price per Meter'],
                    mode='lines+markers', name=location))

# Update figure layout
fig.update_layout(xaxis_title='תאריך',
                  yaxis_title='מחיר למטר',
                  xaxis=dict(tickangle=45),
                  legend=dict(x=0, y=1, traceorder="normal"),width=1300, height=800)
st.markdown("<h3 style='text-align: center; color: black;'>מחיר למטר לאורך זמן עבור מיקומים נבחרים</h3>", unsafe_allow_html=True)

st.plotly_chart(fig,use_container_width=True)

################################# box plot ###########################################
st.write("""
<style>
    .rtl {
        direction: rtl;
        text-align: right;
    }
    font-size: 45px;
</style>
""", unsafe_allow_html=True)
st.write("<div class='rtl'><p style='font-size: 25px;'>בחר מיקום על מנת להציג מדדים</p></div>", unsafe_allow_html=True)

uniselect_locaion = st.selectbox('',df['Location'].unique(),key='location' )
# Selecting the columns for box plot
columns = ['Number of Apartments', 
           'Registered',
           'non-Natives Chance to win',
           'Apartments for Natives', 
           'Registered Natives', 
           'Natives Chance to win']

# # Plotting
# fig, ax = plt.subplots()
# sns.boxplot(data=df.loc[df['Location']==uniselect_locaion,columns], ax=ax)
# ax.set_xticklabels(ax.get_xticklabels(), rotation=45)  # Rotate x-axis labels for better visibility
# Create layout for 2 rows, each with 3 columns
col1, col2, col3 = st.columns(3)
# Plot each feature in its own 
# for i, column in enumerate(columns):
for col, feature in zip([col1, col2, col3,col1, col2, col3], columns):
    fig, ax = plt.subplots()
    sns.boxplot(data=df.loc[df['Location']==uniselect_locaion,feature], ax=ax) 
    ax.set_title(feature)  # Set title as the feature name
    with col:
        st.pyplot(fig)

