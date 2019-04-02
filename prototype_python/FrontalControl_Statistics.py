import numpy as np
import pandas as pd
import neurokit as nk
import statsmodels.formula.api as smf
import statsmodels.api as sm

# =============================================================================
# Part 1
# =============================================================================
def process_processing_speed(data=None, summary=False):
    if data is None:
        data = pd.read_csv("../data/S0_ProcessingSpeed.csv")

    data = data.copy()
    data.loc[:,'Right_Bias'] = np.where(data.loc[:,'Stimulus_Side']=='RIGHT', "RIGHT", "LEFT")
    data.loc[:,'Previous_Response'] = np.where(data.loc[:,'Previous_Response'].isnull(), "NO", "YES")
    data.loc[:,'Previous_RT'] = np.where(data.loc[:,'Previous_Response']=='YES', data['Previous_RT'], 0)
    data.loc[:,'Error'] = np.where(data.loc[:,'Response']!="DOWN", "YES", "NO")

    n_impulsive = sum(data['Previous_Response'] == "YES")/len(data)
    # RT ----------------------------------------------------------------------
    # Filter where response is correct
    df_correct = data.loc[np.where(data['Error']=="NO")]
    n_incorect = (len(data) - len(df_correct))/len(data)
    n_incorect = (len(data) - len(df_correct))/len(data)

    # Remove outliers
    df = df_correct[nk.find_outliers(df_correct["RT"], treshold=2.58) == False].copy()
    n_outliers = (len(df_correct) - len(df))/len(df_correct)


    # StatModels
    formula = 'RT ~ Trial_Order + I(Trial_Order ** 2.0) + ITI + I(ITI ** 2.0) + Right_Bias'
    if len(df[df['Previous_Response'] == "YES"])/len(df) > 0.2:
        formula +=  '+ Previous_Response + Previous_Response:Previous_RT'

    model = smf.ols(formula, data=df).fit()
#    model = smf.rlm(formula, data=df).fit()  # Robust version
#    model = smf.quantreg(formula, data=df).fit()

    # Analyze ITI
    iti_ref = pd.DataFrame({"Trial_Order": [1]*1000,
                        "ITI": np.linspace(np.min(df["ITI"]), np.max(df["ITI"]), 1000),
                        "Right_Bias": ["LEFT"]*1000,
                        "Previous_Response": ["NO"]*1000,
                        "Previous_RT": [0]*1000})
    iti_ref["RT"] = model.predict(iti_ref)
    pred_iti = model.get_prediction(iti_ref)
    pred_iti = pd.concat([iti_ref, pred_iti.summary_frame(alpha=0.05)], axis=1)
    iti_min = pred_iti["mean"].idxmin()

    # Analyze Order
    order_ref = pd.DataFrame({"Trial_Order": np.linspace(np.min(df["Trial_Order"]), np.max(df["Trial_Order"]), 1000),
                        "ITI": iti_min,
                        "Right_Bias": ["LEFT"]*1000,
                        "Previous_Response": ["NO"]*1000,
                        "Previous_RT": [0]*1000})
    order_ref["RT"] = model.predict(order_ref)
    pred_order = model.get_prediction(order_ref)
    pred_order = pd.concat([order_ref, pred_order.summary_frame(alpha=0.05)], axis=1)
    order_min = pred_order["mean"].idxmin()


    # Plot and summary
    if summary is True:
        model.summary()
        iti_ref.plot(x="ITI", y="RT")
        pred_order.plot(x="Trial_Order", y="RT")

    # Indices
    results = {
            "ProcessingSpeed_n_Incorrect": n_incorect,
            "ProcessingSpeed_n_Outliers": n_outliers,
            "ProcessingSpeed_n_Impulsive": n_impulsive,

            "ProcessingSpeed_RT_Accuracy": model.rsquared,
            "ProcessingSpeed_RT_Learning": model.params["Trial_Order"]/df["RT"].std(),
            "ProcessingSpeed_RT_Learning_Significant": model.pvalues["Trial_Order"],
            "ProcessingSpeed_RT_Engagement": model.params["ITI"]/df["RT"].std(),
            "ProcessingSpeed_RT_Engagement_Significant": model.pvalues["ITI"],
            "ProcessingSpeed_RT_RightBias": model.params["Right_Bias[T.RIGHT]"]/df["RT"].std(),
            "ProcessingSpeed_RightBias_Significant": model.pvalues["Right_Bias[T.RIGHT]"],

            "ProcessingSpeed_RT_ITI_Optimal": pred_iti["ITI"][iti_min],
            "ProcessingSpeed_RT": pred_iti["mean"][iti_min],
            "ProcessingSpeed_RT_SE": pred_iti["mean_se"][iti_min],
            "ProcessingSpeed_RT_CI_low": pred_iti["mean_ci_lower"][iti_min],
            "ProcessingSpeed_RT_CI_high": pred_iti["mean_ci_upper"][iti_min],

            "ResponseSelection_RT_Raw_Mean": df["RT"].mean(),
            "ResponseSelection_RT_Raw_SD": df["RT"].std(),

            "ProcessingSpeed_RT_Fatigue": pred_order["Trial_Order"][order_min]}
    return(results)










# =============================================================================
# Part 2
# =============================================================================
def process_response_selection(data=None, summary=False):
    if data is None:
        data = pd.read_csv("../data/S0_ResponseSelection.csv")

    data = data.copy()
    data.loc[:,'Right_Bias'] = np.where(data.loc[:,'Stimulus_Side']=='RIGHT', "RIGHT", "LEFT")
    data.loc[:,'Previous_Response'] = np.where(data.loc[:,'Previous_Response'].isnull(), "NO", "YES")
    data.loc[:,'Previous_RT'] = np.where(data.loc[:,'Previous_Response']=='YES', data['Previous_RT'], 0)
    data.loc[:,'Error'] = np.where(data.loc[:,'Response']!=data.loc[:,'Stimulus_Side'], "YES", "NO")
    data.loc[:,'Error_Previous'] = np.where(data.loc[:,'Error'].shift(-1) == 1, "YES", "NO")


    n_impulsive = sum(data['Previous_Response'] == "YES")/len(data)
    # RT ----------------------------------------------------------------------
    # Filter where response is correct
    df_correct = data.loc[np.where(data['Error']=="NO")]
    n_incorect = (len(data) - len(df_correct))/len(data)

    # Remove outliers
    df = df_correct[nk.find_outliers(df_correct["RT"], treshold=2.58) == False].copy()
    n_outliers = (len(df_correct) - len(df))/len(df_correct)


    # StatModels
    formula = 'RT ~ Trial_Order + I(Trial_Order ** 2.0) + ITI + I(ITI ** 2.0) + Right_Bias'
    if len(df[df['Error'] == "YES"])/len(df) > 0.2:
        formula +=  ' + Error_Previous'
    if len(df[df['Previous_Response'] == "YES"])/len(df) > 0.2:
        formula +=  ' + Previous_Response + Previous_Response:Previous_RT'

    model = smf.ols(formula, data=df).fit()
#    model = smf.rlm(formula, data=df).fit()  # Robust version
#    model = smf.quantreg(formula, data=df).fit()

    # Analyze ITI
    iti_ref = pd.DataFrame({"Trial_Order": [1]*1000,
                        "ITI": np.linspace(np.min(df["ITI"]), np.max(df["ITI"]), 1000),
                        "Right_Bias": ["LEFT"]*1000,
                        "Error_Previous": ["NO"]*1000,
                        "Previous_Response": ["NO"]*1000,
                        "Previous_RT": [0]*1000})
    iti_ref["RT"] = model.predict(iti_ref)
    pred_iti = model.get_prediction(iti_ref)
    pred_iti = pd.concat([iti_ref, pred_iti.summary_frame(alpha=0.05)], axis=1)
    iti_min = pred_iti["mean"].idxmin()

    # Analyze Order
    order_ref = pd.DataFrame({"Trial_Order": np.linspace(np.min(df["Trial_Order"]), np.max(df["Trial_Order"]), 1000),
                        "ITI": iti_min,
                        "Right_Bias": ["LEFT"]*1000,
                        "Previous_Response": ["NO"]*1000,
                        "Previous_RT": [0]*1000,
                        "Error_Previous": ["NO"]*1000})
    order_ref["RT"] = model.predict(order_ref)
    pred_order = model.get_prediction(order_ref)
    pred_order = pd.concat([order_ref, pred_order.summary_frame(alpha=0.05)], axis=1)
    order_min = pred_order["mean"].idxmin()


    # Plot and summary
    if summary is True:
        model.summary()
        pred_iti.plot(x="ITI", y="RT")
        pred_order.plot(x="Trial_Order", y="RT")

    # Indices
    results = {
            "ResponseSelection_n_Incorrect": n_incorect,
            "ResponseSelection_n_Outliers": n_outliers,
            "ResponseSelection_n_Impulsive": n_impulsive,

            "ResponseSelection_RT_Accuracy": model.rsquared,
            "ResponseSelection_RT_Learning": model.params["Trial_Order"]/df["RT"].std(),
            "ResponseSelection_RT_Learning_Significant": model.pvalues["Trial_Order"],
            "ResponseSelection_RT_Engagement": model.params["ITI"]/df["RT"].std(),
            "ResponseSelection_RT_Engagement_Significant": model.pvalues["ITI"],
            "ResponseSelection_RT_RightBias": model.params["Right_Bias[T.RIGHT]"]/df["RT"].std(),
            "ResponseSelection_RightBias_Significant": model.pvalues["Right_Bias[T.RIGHT]"],

            "ResponseSelection_RT_ITI_Optimal": pred_iti["ITI"][iti_min],
            "ResponseSelection_RT": pred_iti["mean"][iti_min],
            "ResponseSelection_RT_SE": pred_iti["mean_se"][iti_min],
            "ResponseSelection_RT_CI_low": pred_iti["mean_ci_lower"][iti_min],
            "ResponseSelection_RT_CI_high": pred_iti["mean_ci_upper"][iti_min],

            "ResponseSelection_RT_Raw_Mean": df["RT"].mean(),
            "ResponseSelection_RT_Raw_SD": df["RT"].std(),
#            "ResponseSelection_RT_Raw_Min": df["RT"].min(),
#            "ResponseSelection_RT_Raw_Max": df["RT"].max(),
#            "ResponseSelection_RT_Raw_Percentile_025": df["RT"].quantile(0.025),
#            "ResponseSelection_RT_Raw_Percentile_975": df["RT"].quantile(0.975),

            "SSRT_Min": 16.66667,
            "SSRT_Max": df["RT"].quantile(0.10),

            "ResponseSelection_RT_Fatigue": pred_order["Trial_Order"][order_min]}

    if "Error_Previous[T.YES]" in model.params.index:
        results["ResponseSelection_RT_PreviousError"] = model.params["Error_Previous[T.YES]"]/df["RT"].std()
        results["ResponseSelection_RT_PreviousError_Significant"] = model.pvalues["Error_Previous[T.YES]"]


    # COMBINED INDICES --------------------------------------------------------
    # IES: Inverse Efficiency Score (Bruyer & Brysbaert, 2011)
    if 1-n_incorect > 0:
        results["IES"] = df["RT"].mean()/(1-n_incorect)
        results["IES_Corrected"] = results["ResponseSelection_RT"]/(1-n_incorect)

    # Throughput (Thorne, 2006)
    results["Throughput"] = (1-n_incorect)/data["RT"].mean()*600

    # ERRORS ------------------------------------------------------------------
    if(n_incorect) > 0.1 and len(data[data['Error'] == "YES"]) > 3:
        # StatModels
        formula = 'Error ~ Trial_Order + I(Trial_Order ** 2.0) + ITI + I(ITI ** 2.0) + Right_Bias'


        model = smf.glm(formula=formula, data=data, family=sm.families.Binomial()).fit(disp=0)
        if len(data[data['Error'] == "YES"])/len(data) > 0.2:
            formula +=  ' + Error_Previous'
        if len(data[data['Previous_Response'] == "YES"])/len(data) > 0.2:
            formula +=  ' + Previous_Response + Previous_Response:Previous_RT'


        # Analyze ITI
        iti_ref = pd.DataFrame({"Trial_Order": [1]*1000,
                            "ITI": np.linspace(np.min(df["ITI"]), np.max(df["ITI"]), 1000),
                            "Right_Bias": ["LEFT"]*1000,
                            "Previous_Response": ["NO"]*1000,
                            "Previous_RT": [0]*1000,
                            "Error_Previous": ["NO"]*1000})
        iti_ref["Error"] = model.predict(iti_ref)
        pred_iti = model.get_prediction(iti_ref)
        pred_iti = pd.concat([iti_ref, pred_iti.summary_frame(alpha=0.05)], axis=1)
        iti_min = pred_iti["mean"].idxmin()

        # Analyze Order
        order_ref = pd.DataFrame({"Trial_Order": np.linspace(np.min(df["Trial_Order"]), np.max(df["Trial_Order"]), 1000),
                            "ITI": iti_min,
                            "Right_Bias": ["LEFT"]*1000,
                            "Previous_Response": ["NO"]*1000,
                            "Previous_RT": [0]*1000,
                            "Error_Previous": ["NO"]*1000})
        order_ref["Error"] = model.predict(order_ref)
        pred_order = model.get_prediction(order_ref)
        pred_order = pd.concat([order_ref, pred_order.summary_frame(alpha=0.05)], axis=1)
        order_min = pred_order["mean"].idxmin()


        # Plot and summary
        if summary is True:
            model.summary()
            pred_iti.plot(x="ITI", y="Error")
            pred_order.plot(x="Trial_Order", y="Error")

        results["ResponseSelection_Error_ITI_Optimal"] = pred_iti["ITI"][iti_min]
        results["ResponseSelection_Error"] = pred_iti["mean"][iti_min]
        results["ResponseSelection_Error_SE"] = pred_iti["mean_se"][iti_min]
        results["ResponseSelection_Error_CI_low"] = pred_iti["mean_ci_lower"][iti_min]
        results["ResponseSelection_Error_CI_high"] = pred_iti["mean_ci_upper"][iti_min]

    return(results)











# =============================================================================
# Part 2
# =============================================================================
def process_response_inhibition(data=None, summary=False):
    if data is None:
        data = pd.read_csv("../data/S0_ResponseInhibition.csv")

    data = data.copy()
    data.loc[:,'Right_Bias'] = np.where(data.loc[:,'Stimulus_Side']=='RIGHT', "RIGHT", "LEFT")
    data.loc[:,'Previous_Response'] = np.where(data.loc[:,'Previous_Response'].isnull(), "NO", "YES")
    data.loc[:,'Previous_RT'] = np.where(data.loc[:,'Previous_Response']=='YES', data['Previous_RT'], 0)
    data['Error'] = "NO"
    data.loc[data["Stop_Signal"] == False,'Error'] = np.where(data.loc[data["Stop_Signal"] == False,'Response']!=data.loc[data["Stop_Signal"] == False,'Stimulus_Side'], "YES", "NO")
    data.loc[data["Stop_Signal"] == True,'Error'] = np.where(
             (data.loc[data["Stop_Signal"] == True,'Response']=="Time_Max_Exceeded") |
             (data.loc[data["Stop_Signal"] == True,'RT'] < data.loc[data["Stop_Signal"] == True,'Stop_Signal_RT']),
             "NO", "YES")
    data.loc[:,'Error_Previous'] = np.where(data.loc[:,'Error'].shift(-1) == 1, "YES", "NO")


    n_impulsive = sum(data['Previous_Response'] == "YES")/len(data)
    n_incorect = sum(data['Error'] == "YES")/len(data)
    # Inhibition ----------------------------------------------------------------------
    df_inhib = data.loc[np.where(data['Stop_Signal']==True)]
    n_inhibError = sum(df_inhib['Error'] == "YES")/len(df_inhib)


    if(n_inhibError) > 0.1:
        # StatModels
        formula = 'Error ~ Stop_Signal_RT'
        if n_incorect > 0.2:
            formula +=  '+ Error_Previous'
        if n_impulsive > 0.2:
            formula +=  '+ Previous_Response + Previous_Response:Previous_RT'

        model = smf.glm(formula=formula, data=data, family=sm.families.Binomial()).fit(disp=0)

#        # Analyze ITI
#        iti_ref = pd.DataFrame({"Trial_Order": [1]*1000,
#                            "ITI": np.linspace(np.min(df["ITI"]), np.max(df["ITI"]), 1000),
#                            "Right_Bias": ["LEFT"]*1000,
#                            "Previous_Response": ["NO"]*1000,
#                            "Previous_RT": [0]*1000,
#                            "Error_Previous": ["NO"]*1000})
#        iti_ref["Error"] = model.predict(iti_ref)
#        pred_iti = model.get_prediction(iti_ref)
#        pred_iti = pd.concat([iti_ref, pred_iti.summary_frame(alpha=0.05)], axis=1)
#        iti_min = pred_iti["mean"].idxmin()
#
#        # Analyze Order
#        order_ref = pd.DataFrame({"Trial_Order": np.linspace(np.min(df["Trial_Order"]), np.max(df["Trial_Order"]), 1000),
#                            "ITI": iti_min,
#                            "Right_Bias": ["LEFT"]*1000,
#                            "Previous_Response": ["NO"]*1000,
#                            "Previous_RT": [0]*1000,
#                            "Error_Previous": ["NO"]*1000})
#        order_ref["Error"] = model.predict(order_ref)
#        pred_order = model.get_prediction(order_ref)
#        pred_order = pd.concat([order_ref, pred_order.summary_frame(alpha=0.05)], axis=1)
#        order_min = pred_order["mean"].idxmin()

        # Analyze SSRT
        ssrt_ref = pd.DataFrame({"Stop_Signal_RT": np.linspace(np.min(df_inhib["Stop_Signal_RT"]), np.max(df_inhib["Stop_Signal_RT"]), 1000),
                            "Trial_Order": np.linspace(np.min(df_inhib["Trial_Order"]), np.max(df_inhib["Trial_Order"]), 1000),
                            "ITI": 200,
                            "Right_Bias": ["LEFT"]*1000,
                            "Previous_Response": ["NO"]*1000,
                            "Previous_RT": [0]*1000,
                            "Error_Previous": ["NO"]*1000})
        ssrt_ref["Error"] = model.predict(ssrt_ref)
        pred_ssrt = model.get_prediction(ssrt_ref)
        pred_ssrt = pd.concat([ssrt_ref, pred_ssrt.summary_frame(alpha=0.05)], axis=1)
#        order_min = pred_ssrt["mean"].idxmin()


    # Plot and summary
    if summary is True:
        model.summary()
#        pred_iti.plot(x="ITI", y="Error")
#        pred_order.plot(x="Trial_Order", y="Error")
        pred_ssrt.plot(x="Stop_Signal_RT", y="Error")


#    # RT ----------------------------------------------------------------------
#    # Filter where response is correct
#    df_correct = data.loc[np.where(data['Error']=="NO")]
#    n_incorect = (len(data) - len(df_correct))/len(data)
#
#    # Remove outliers
#    df = df_correct[nk.find_outliers(df_correct["RT"], treshold=2.58) == False].copy()
#    n_outliers = (len(df_correct) - len(df))/len(df_correct)
#
#
#    # StatModels
#    formula = 'RT ~ Trial_Order + I(Trial_Order ** 2.0) + ITI + I(ITI ** 2.0) + Right_Bias'
#    if n_incorect > 0.1:
#        formula +=  ' + Error_Previous'
#    if n_impulsive > 0.1:
#        formula +=  ' + Previous_Response + Previous_Response:Previous_RT'
#
#    model = smf.ols(formula, data=df).fit()
##    model = smf.rlm(formula, data=df).fit()  # Robust version
##    model = smf.quantreg(formula, data=df).fit()
#
#    # Analyze ITI
#    iti_ref = pd.DataFrame({"Trial_Order": [1]*1000,
#                        "ITI": np.linspace(np.min(df["ITI"]), np.max(df["ITI"]), 1000),
#                        "Right_Bias": ["LEFT"]*1000,
#                        "Error_Previous": ["NO"]*1000,
#                        "Previous_Response": ["NO"]*1000,
#                        "Previous_RT": [0]*1000})
#    iti_ref["RT"] = model.predict(iti_ref)
#    pred_iti = model.get_prediction(iti_ref)
#    pred_iti = pd.concat([iti_ref, pred_iti.summary_frame(alpha=0.05)], axis=1)
#    iti_min = pred_iti["mean"].idxmin()
#
#    # Analyze Order
#    order_ref = pd.DataFrame({"Trial_Order": np.linspace(np.min(df["Trial_Order"]), np.max(df["Trial_Order"]), 1000),
#                        "ITI": iti_min,
#                        "Right_Bias": ["LEFT"]*1000,
#                        "Previous_Response": ["NO"]*1000,
#                        "Previous_RT": [0]*1000,
#                        "Error_Previous": ["NO"]*1000})
#    order_ref["RT"] = model.predict(order_ref)
#    pred_order = model.get_prediction(order_ref)
#    pred_order = pd.concat([order_ref, pred_order.summary_frame(alpha=0.05)], axis=1)
#    order_min = pred_order["mean"].idxmin()
#
#
#    # Plot and summary
#    if summary is True:
#        model.summary()
#        iti_ref.plot(x="ITI", y="RT")
#        pred_order.plot(x="Trial_Order", y="RT")