# functions for parsing times

# libraries
import numpy as np
import datetime
# the dateparser module is for if you are really lazy and don't know what format your date will be in
# it comes at a cost though, it is incredibly slow (if you do a lot of dateparsing) use at your own risk
# adding a new rule to the duration_hours function like if format="coolwebsite"
# then if there is a comma in time_a make the format "%Y, %m, %d" but else make it %Y %d %m
import dateparser


# computes the next time in an array of times after time x
def next_time(time_x, time_list):
    min_dur_time = '1800-1-1 1:00'
    min_dur = np.inf
    for time_c in time_list:
        print(duration_hours([time_x, time_c]), min_dur)
        if duration_hours([time_x, time_c]) > 0 and duration_hours([time_x, time_c]) < min_dur:
            min_dur_time = time_c
            min_dur = duration_hours([time_x, time_c])
    return min_dur_time


# flexible datetime dt using the modules full capabilities
def duration_hours(t_interval, t_formats=["standard", "standard"]):
    try:
        r_t_formats = t_formats[:]

        # this algorithm tries to find the correct format if none is given
        for i in range(0, len(r_t_formats)):
            if r_t_formats[i] == "standard":
                if '-' in t_interval[i]:
                    r_t_formats[i] = "%Y-%m-%d %H:%M"
                else:
                    r_t_formats[i] = "%m/%d/%Y %H:%M"

        r_t_a = datetime.datetime.strptime(t_interval[0], r_t_formats[0])
        r_t_b = datetime.datetime.strptime(t_interval[1], r_t_formats[1])

        return secs_to_hours((r_t_b - r_t_a).total_seconds())

    except:
        print("ERROR IN TIME DURATION CALCULATION")
        return 0


# slow and lazy :( ;( "()"
def datetime_dt_hours_slow(time_a, time_b):
    r_time_a = dateparser.parse(time_a, languages=['en'])
    r_time_b = dateparser.parse(time_b, languages=['en'])
    return secs_to_hours((r_time_b-r_time_a).total_seconds())


# turns a std time into a military time
def clean_hour_min(std_time):
    if ':' in std_time:
        time_parts = std_time.split(':')
    elif '-' in std_time:
        time_parts = std_time.split('-')
    else:
        time_parts = [std_time[2:len(std_time)], std_time[2:len(std_time)]]
    hours = get_ints(time_parts[0])
    minutes = get_ints(time_parts[1])
    # NOTE, if it is already in military time this step will not be applied
    # because the time wont have a pm in it anyways, so this function always works
    if 'P' in std_time or 'p' in std_time:  # PM
        hours += 12
    return [hours, minutes]


# turns a number of hours into a number of days
def hours_to_days(hours):
    return round(hours/24.0, 3)


# turns seconds into hours
def secs_to_hours(secs):
    return round(secs/3600.0, 3)


# turns a number of hours into a number of (approximate) years
def hours_to_years(hours):
    return round(hours/(24.0*365.3), 1)


# returns all of the integers in a string concatenated together
def get_ints(string, show_errors=True):
    out_int = ''
    for char in string:
        if char.isdigit():
            out_int += char
    if out_int != '':
        return int(out_int)
    else:
        if show_errors:
            print("No integers present")
        return False


# finds and returns the smaller of 2 times
def min_time(times):
    try:
        reference_time = '1800-1-1 1:00'
        time_diffs = []
        for time_b in times:
            if type(time_b) == str:
                if time_b.lower != "null":
                    time_diffs.append(duration_hours([reference_time, time_b]))
        return times[time_diffs.index(min(time_diffs))]
    except TypeError:
        # maximum length, TypeError is thrown if you give it a time that is too short ie. '' or '1' longest might have a better chance of being a real time
        print("Error in min_time")
        return max([len(time) for time in times])
    except:
        print("ERROR in min_time FATAL")
        return max([len(time) for time in times])


# finds and returns the smaller of 2 times
def max_time(times):
    try:
        reference_time = '1800-1-1 1:00'
        time_diffs = []
        for time_b in times:
            if type(time_b) == str:
                if time_b.lower != "null":
                    time_diffs.append(duration_hours([reference_time, time_b]))
        return times[time_diffs.index(max(time_diffs))]
    except TypeError:
        # maximum length, TypeError is thrown if you give it a time that is too short ie. '' or '1' longest might have a better chance of being a real time
        print("Error in min_time")
        return max([len(time) for time in times])
    except:
        print("ERROR in min_time FATAL")
        return max([len(time) for time in times])


# sorts times chronologically
def sort_times_chron(time_list):
    ordered_times = []
    times_left = time_list[:]
    for i in range(0, len(time_list)):
        cur_smallest_time = min_time(times_left)
        ordered_times.append(cur_smallest_time)
        times_left.pop(times_left.index(cur_smallest_time))
    return ordered_times


# gives the indices necessary to sort the times chronologically
def time_chron_indices(time_list):
    ordered_indices_correct = []
    times_left = time_list[:]
    for i in range(0, len(time_list)):
        cur_smallest_time = min_time(times_left)
        for j in range(0, len(time_list)):
            if time_list[j] == cur_smallest_time and j not in ordered_indices_correct:
                ordered_indices_correct.append(j)
        times_left.pop(times_left.index(cur_smallest_time))
    return ordered_indices_correct


# returns whether or not a time is inside a time range (standard times)
def time_in_range(time, time_range):
    if duration_hours([time, time_range[0]]) * duration_hours([time, time_range[1]]) < 0:
        return True
    else:
        return False


# mark indices of an array of times as out of a time range all times are standard times
def time_confine_range(times, time_range):
    toss_indices = []
    for i in range(0, len(times)):
        if not time_in_range(times[i], time_range):
            toss_indices.append(i)
    return toss_indices


# returns the "inverse" of an array of indices, given the max length
def invert_indices_array(indices, max_length):
    out_indices = []
    for i in range(0, max_length):
        if i not in indices:
            out_indices.append(i)
    return out_indices


# takes multiple arrays of values which are connected and updates all of them keeping the
# values with specific indices and keeping them together. The times are organized and ones out side of a
# range are thrown out. Time must be provided as the times and in the all_stats list
def time_order_keeper(times, all_stats, valid_t_range):
    out_stats = []
    # toss dates out of range
    good_times_in_range = invert_indices_array(time_confine_range(times, valid_t_range), len(times))
    for i in range(0, len(all_stats)):
        out_stats.append([all_stats[i][good_time_in_range] for good_time_in_range in good_times_in_range])
    times_in_range = [times[good_time_in_range] for good_time_in_range in good_times_in_range]

    # organize data by dates
    ordered_time_indices = time_chron_indices(times_in_range)
    for i in range(0, len(out_stats)):
        out_stats[i] = [out_stats[i][ordered_time_index] for ordered_time_index in ordered_time_indices]

    return out_stats



