def check_if_pump_needs_on(settings_data, new_data, action_cause):
    min_temp = settings_data[2]
    max_temp = settings_data[3]
    min_water_level = settings_data[4]
    max_water_level = settings_data[5]
    pH_level = settings_data[6]
    DO_level = settings_data[7]

    temperature = new_data[0]
    new_pH_level = new_data[3]
    new_water_level = new_data[2]
    new_DO_level = new_data[1]

    return_status = False
    statuses = []

    if min_temp < temperature and temperature < max_temp:
        statuses.append(0)
    else:
        action_cause += f" temp not within set range: {min_temp} < {temperature} < {max_temp},"
        statuses.append(1)

    if min_water_level < new_water_level and new_water_level < max_water_level:
        statuses.append(0)
    else:
        action_cause += f" water level not within set range: {min_water_level} < {new_water_level} < {max_water_level},"
        statuses.append(1)

    if (pH_level - 1) < new_pH_level and new_pH_level < (pH_level + 1):
        statuses.append(0)
    else:
        action_cause += f" pH level not within set range: ({pH_level - 1}) < {new_pH_level} < ({pH_level + 1}),"
        statuses.append(1)

    # uncomment the following line if DO is attached

    # if (DO_level - 1) < new_DO_level and new_DO_level < (DO_level + 1):
    #     statuses.append(0)
    # else:
    #     action_cause += " pH level not within set range,"
    #     statuses.append(1)
    if 1 in statuses:
        return_status = True

    return return_status, action_cause


def check_if_sols_needs_on(settings_data, new_data, action_cause):
    min_temp = settings_data[2]
    max_temp = settings_data[3]
    min_water_level = settings_data[4]
    max_water_level = settings_data[5]
    pH_level = settings_data[6]
    DO_level = settings_data[7]

    temperature = new_data[0]
    new_pH_level = new_data[3]
    new_water_level = new_data[2]
    new_DO_level = new_data[1]

    sol_in = False
    sol_in_statuses = []
    sol_out = False
    sol_out_statuses = []

    if temperature < min_temp:
        action_cause += f" water temp below minimum: {temperature} < {min_temp},"
        sol_in_statuses.append(1)
        sol_out_statuses.append(1)
    else:
        sol_in_statuses.append(0)
        sol_out_statuses.append(0)

    if new_water_level < min_water_level:
        action_cause += f" water level below minimum: {new_water_level} < {min_water_level},"
        sol_in_statuses.append(1)
        sol_out_statuses.append(0)
    elif new_water_level > max_water_level:
        action_cause += " water level above maximum,"
        sol_in_statuses.append(0)
        sol_out_statuses.append(1)
    else:
        sol_in_statuses.append(0)
        sol_out_statuses.append(0)

    if (pH_level - 1) < new_pH_level and new_pH_level < (pH_level + 1):
        sol_in_statuses.append(0)
        sol_out_statuses.append(0)
    else:
        action_cause += f" water pH not within range: ({pH_level - 1}) < {new_pH_level} < ({pH_level + 1}),"
        sol_in_statuses.append(1)
        sol_out_statuses.append(1)

    # uncomment the following line if DO is attached

    # if (DO_level - 1) < new_DO_level < (DO_level + 1):
    #     sol_in_statuses.append(0)
    #     sol_out_statuses.append(0)
    # else:
    #     action_cause += " water DO not within range,"
    #     sol_in_statuses.append(1)
    #     sol_out_statuses.append(1)

    if 1 in sol_in_statuses:
        sol_in = True
    if 1 in sol_out_statuses:
        sol_out = True

    return sol_in, sol_out, action_cause
