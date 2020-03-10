
      LookedUpValue = LOOKUPVALUE(LookupTable[LookupColumnToReturn],LookupTable[LookupColumnValue],CurrentTable[ColumnForLookup])
      
  Example:
      
      AccountName = LookupValue(Account[Name],Account[Id],Order[CustomerId])
      
  Returns the accountName using the Account.Id based on the CustomerId in the OrderTable
