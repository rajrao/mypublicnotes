https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-sql-filter

**System properties**
1. sys.SessionId like '%xxxx-yyyy%' 
1. sys.SessionId = 'xxxxx' 
1. sys.messageid = 'xxxx'
1. sys.correlationid like 'abc-%'
1. sys.label is not null


**Message properties**
1. propertyX = 'A'
1. "propertyX" = 'A'
1. "property X" = 'A'
1. MessagePropertyA > 1
1. MessagePropertyA > 2.08
1. MessageProperty1 = 1 and MessageProperty2 = 3
1. MessageProperty1 = 1 or MessageProperty2 = 3
1. MessageProperty1 - MessageProperty2 = 80
1. Exists(MessageProperty23)
1. Exists(\"Message Property AA\")
1. MessageProperty1 like 'SuperMan%'
1. MessageProperty1 IS NULL
1. MessageProperty1 IS NOT NULL

When message property name has special characters (example from Dyanmics CRM, where "http://schemas.microsoft.com/xrm/2011/Claims/EntityLogicalName" is the name of the message property)
"http://schemas.microsoft.com/xrm/2011/Claims/EntityLogicalName" = 'account'

**Parameter based filters** (where DateTimeMp is a message property of type DateTime and @dtParam is a param passed to the filter as a DateTime object)

    var filter = new SqlFilter("datetime >= @dtParam");
    filter.Parameters.Add("@dtParam", DateTime.Parse("2020-10-23"));

1. DateTimeMp < @dtParam
1. DateTimeMp > @dtParam
1. (DateTimeMp2-DateTimeMp1) <= @timespan //@timespan is a parameter of type TimeSpan
1. DateTimeMp2-DateTimeMp1 <= @timespan


