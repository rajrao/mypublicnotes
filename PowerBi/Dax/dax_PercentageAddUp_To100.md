An example of how to calculate Percentage that adds up to a 100.

Relationship of tables


    ┌──────────────────┐
    │ Survey Questions ├───┐
    └──────────────────┘   │
                           │
                           │
                           │
               ┌───────────▼───────┐
               │ Survey Responses  │
               └───────────────────┘



Survey Question has list of questions asked.
Survey Responses has responses for the questions. The response can be Agree, Neutral, Disagree.
When the addition does not add up to 100, the remaining is assigned to Neutral.

```
Number of Responses % = 
VAR totalCountForQuestion =
    CALCULATE (
        COUNT ( 'Survey Responses'[Response Id] ),
        REMOVEFILTERS ( 'Survey Responses' ),
        KEEPFILTERS ( 'Survey Questions' )
    )
VAR countForQuestionAgreeResponseAgree =
    CALCULATE (
        COUNT ( 'Survey Responses'[Response Id] ),
        KEEPFILTERS ( 'Survey Questions' ),
        ALL ( 'Survey Responses' ),
        'Survey Responses'[Response] == "Agree"
    )
VAR countForQuestionAgreeResponseNeutral =
    CALCULATE (
        COUNT ( 'Survey Responses'[Response Id] ),
        KEEPFILTERS ( 'Survey Questions' ),
        ALL ( 'Survey Responses' ),
        'Survey Responses'[Response] == "Neutral"
    )
VAR countForQuestionAgreeResponseDisagree =
    CALCULATE (
        COUNT ( 'Survey Responses'[Response Id] ),
        KEEPFILTERS ( 'Survey Questions' ),
        ALL ( 'Survey Responses' ),
        'Survey Responses'[Response] == "Disagree"
    )
VAR percentageCalAgree =
    ROUND ( ( countForQuestionAgreeResponseAgree / totalCountForQuestion ), 2 )
VAR percentageCalDisagree =
    ROUND ( ( countForQuestionAgreeResponseDisagree / totalCountForQuestion ), 2 )
VAR percentageCalNeutral = 1 - percentageCalAgree - percentageCalDisagree
VAR outputValue =
    SWITCH (
        SELECTEDVALUE ( 'Survey Responses'[Response] ),
        "Agree", percentageCalAgree,
        "Disagree", percentageCalDisagree,
        "Neutral", percentageCalNeutral,
        percentageCalAgree + percentageCalDisagree + percentageCalNeutral
    )
RETURN
    outputValue

```
