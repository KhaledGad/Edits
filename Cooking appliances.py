# Cooking appliances

# importing functions
from ramp import User,UseCase,calc_peak_time_range,yearly_pattern
import pandas as pd

user_1 = User(
    user_name = "Household with single lunch habit",
    num_users = 1,
    user_preference = 1, # user_1 has only one lunch preference
)

user_2 = User(
    user_name = "Household with different lunch habit",
    num_users = 1,
    user_preference = 3, # user_2 has 3 lunch preferences
)

# soup for lunch
soup_1 = user_1.add_appliance(
    name = "soup for lunch",
    power = 1200,
    func_time = 25,
    func_cycle = 25,
    thermal_p_var = 0.2,
    fixed_cycle = 1,
    window_1 = [12*60,15*60],
    p_11 = 1200,   # power of the first cycle
    t_11 = 5,      # time needed for the first cycle
    p_12 = 750,    # power of the second cycle
    t_12 = 20,     # time needed for the second cycle
    cw11 = [12*60,15*60]
)

# soup for lunch
soup_2 = user_2.add_appliance(
    name = "soup for lunch",
    power = 1200,
    func_time = 25,
    func_cycle = 25,
    # thermal_p_var = 0.2,
    fixed_cycle = 1,
    pref_index = 1, # the first preference
    window_1 = [12*60,15*60],
    p_11 = 1200,   # power of the first cycle
    t_11 = 5,      # time needed for the first cycle
    p_12 = 750,    # power of the second cycle
    t_12 = 20,     # time needed for the second cycle
    cw11 = [12*60,15*60]
)

# rice for lunch
rice_2 = user_2.add_appliance(
    name = "rice for lunch",
    power = 1200,
    func_time = 15,
    func_cycle = 15,
    # thermal_p_var = 0.2,
    pref_index = 2,  # the second preference
    fixed_cycle = 1,
    window_1 = [12*60,15*60],
    p_11 = 1200,   # power of the first cycle
    t_11 = 5,      # time needed for the first cycle
    p_12 = 600,    # power of the second cycle
    t_12 = 10,     # time needed for the second cycle
    cw11 = [12*60,15*60]

)

# # new meal
new_meal = user_2.add_appliance(
    name = "rice for lunch",
    power = 5000,
    func_time = 15,
    func_cycle = 15,
    # thermal_p_var = 0.2,
    pref_index = 3,  # the second preference
    fixed_cycle = 1,
    window_1 = [12*60,15*60],
    p_11 = 1200,   # power of the first cycle
    t_11 = 5,      # time needed for the first cycle
    p_12 = 600,    # power of the second cycle
    t_12 = 10,     # time needed for the second cycle
    cw11 = [12*60,15*60]

)

# new_meal_2 = user_2.add_appliance(
#     name = "rice for lunch",
#     power = 6000,
#     func_time = 15,
#     func_cycle = 15,
#     # thermal_p_var = 0.2,
#     pref_index = 2,  # the second preference
#     fixed_cycle = 1,
#     window_1 = [12*60,15*60],
#     p_11 = 1200,   # power of the first cycle
#     t_11 = 5,      # time needed for the first cycle
#     p_12 = 600,    # power of the second cycle
#     t_12 = 10,     # time needed for the second cycle
#     cw11 = [12*60,15*60]

# )


# you can have an overview of data inputs by usering User.export_to_dataframe method
# user_lunch = UseCase(users=[user_1,user_2])
user_lunch = UseCase(users=[user_2])

x = user_lunch.export_to_dataframe().T
# x.to_csv('output.csv', index=True)

peak_time_range = calc_peak_time_range(
    user_list = user_lunch.users
)
year_behaviour = yearly_pattern()

# number of days
n_days = 8

# storing all the profiles for all the users
profiles = pd.DataFrame(index = pd.date_range(start = "2020-01-01",periods = 1440*n_days,freq="T"))

for user in user_lunch.users:

    # storing daily profiles for a user
    user_profiles = []
    for day in range(n_days):
        single_profile = user.generate_single_load_profile(
            prof_i = day, # the day to generate the profile
            peak_time_range = peak_time_range,
            day_type = year_behaviour
        )

        user_profiles.extend(single_profile)

    profiles[user.user_name] = user_profiles
    
profiles.resample("1d").sum().plot(title = "daily energy consumption")
