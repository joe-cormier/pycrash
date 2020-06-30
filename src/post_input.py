

def post_input(v_num):
    """
    interpolate steering wheel angle, throttle and brake data for post impact motion
    """

    if v_num == 1:
        vdf = v1_post  # detailed input from EDR type data
    if v_num == 2:
        vdf =v2_post   # detailed input from EDR type data

    # Create column vector for time at interval dt. Length will be determined by initial  time of input data and zero
    t = list(np.arange(0,vdf.input_t.max()+dt,dt))                                    # first time in df will be 0

    df = pd.DataFrame()                                                             # create dataframe for vehicle input with interpolated values
    df['t'] = t

    # merge dataframe time column with input file by its time column
    vdf['input_t'] = vdf.input_t.round(3)  # force two time columns to have the same number of significant digits
    df['t'] = df.t.round(3)
    df = pd.merge(df, vdf, how = 'left', left_on = 't', right_on = 'input_t')
    df = df.interpolate(method = 'linear') # interpolate NaN values left after merging
    df = df.drop(columns = ['input_t', 't'])  # drop input time column
    df['t'] = t # reset time column due to interpolating
    df['t'] = df.t.round(3) # reset signficant digits

    df_in = df  # reasign dataframe and delete old variables
    del df, vdf, t
    df_in = df_in.reset_index(drop = True)

    return df_in
