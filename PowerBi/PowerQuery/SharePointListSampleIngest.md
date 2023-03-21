```
let
  Source = SharePoint.Tables("https://xxxxx.sharepoint.com/sites/PowerBICoE", [Implementation= "2.0", ViewMode = "Default"]),
  Navigation = Source{[Title = "Name Of List"]}[Items],
  TableSchema = Table.Schema(Navigation),
  UserMultiTypeRows = Table.SelectRows(TableSchema, each [NativeTypeName] = "UserMulti"),
  UserMultiFieldNames = {"id", "value", "title", "email", "sip", "picture", "jobTitle", "department"},
  UserMultiTransforms = Table.AddColumn(UserMultiTypeRows, "UserMultiTransform", each(name) => 
                    if (name <> "") then @Text.Combine(Table.Column(Table.FromList(name, Record.FieldValues, UserMultiFieldNames), "title"), ", ") else null, Function.Type),
  UserMultiChanges = Table.ToRows(Table.SelectColumns(UserMultiTransforms, { "Name","UserMultiTransform"})),
  ExpandedUserMulti = Table.TransformColumns(Navigation, UserMultiChanges, null, MissingField.UseNull),
  UserTypeRows = Table.SelectRows(TableSchema, each [NativeTypeName] = "User"),
  UserFieldNames = {"id", "title", "email", "sip", "picture", "jobTitle", "department"},
  UserTransforms = Table.AddColumn(UserTypeRows, "UserTransform", each(name) => 
                    if (name <> "") then @Text.Combine(Table.Column(Table.FromList(name, Record.FieldValues, UserFieldNames), "title"), ", ") else null, Function.Type),
  UserChanges = Table.ToRows(Table.SelectColumns(UserTransforms, { "Name","UserTransform"})),
  ExpandedUser = Table.TransformColumns(ExpandedUserMulti, UserChanges, null, MissingField.UseNull),
  LookupTypeRows = Table.SelectRows(TableSchema, each [NativeTypeName] = "Lookup"),
  LookupFieldNames = {"lookupId", "lookupValue", "isSecretFieldValue"},
  LookupTransforms = Table.AddColumn(LookupTypeRows, "LookupTransform", each(name) => 
                    if (name <> "") then @Text.Combine(Table.Column(Table.FromList(name, Record.FieldValues, LookupFieldNames), "lookupValue"), ", ") else null, Function.Type),
  LookupChanges = Table.ToRows(Table.SelectColumns(LookupTransforms, { "Name","LookupTransform"})),
  ExpandedLookup = Table.TransformColumns(ExpandedUser, LookupChanges, null, MissingField.UseNull),
  TaxonomyFieldTypeTypeRows = Table.SelectRows(TableSchema, each [NativeTypeName] = "TaxonomyFieldType"),
  TaxonomyFieldTypeTransforms = Table.AddColumn(TaxonomyFieldTypeTypeRows, "TaxonomyFieldTypeTransform", each (name) => 
                        if (name <> "") then @Text.Combine(Table.Column(Table.FromRecords({ name }), "Label")) else null, Function.Type),
  TaxonomyFieldTypeChanges = Table.ToRows(Table.SelectColumns(TaxonomyFieldTypeTransforms, { "Name","TaxonomyFieldTypeTransform"})),
  ExpandedTaxonomyFieldType = Table.TransformColumns(ExpandedLookup, TaxonomyFieldTypeChanges, null, MissingField.UseNull),
  LocationTypeRows = Table.SelectRows(TableSchema, each [NativeTypeName] = "Location"),
  LocationTransforms = Table.AddColumn(LocationTypeRows, "LocationTransform", each (name) => 
                        if (name <> "") then @Text.Combine(Table.Column(Table.FromRecords({ name }), "DisplayName")) else null, Function.Type),
  LocationChanges = Table.ToRows(Table.SelectColumns(LocationTransforms, { "Name","LocationTransform"})),
  ExpandedLocation = Table.TransformColumns(ExpandedTaxonomyFieldType, LocationChanges, null, MissingField.UseNull),
  ThumbnailTypeRows = Table.SelectRows(TableSchema, each [NativeTypeName] = "Thumbnail"),
  ThumbnailTransforms = Table.AddColumn(ThumbnailTypeRows, "ThumbnailTransform", each (name) => 
                        if (name <> "") then @Text.Combine(Table.Column(Table.FromRecords({ name }), "fileName")) else null, Function.Type),
  ThumbnailChanges = Table.ToRows(Table.SelectColumns(ThumbnailTransforms, { "Name","ThumbnailTransform"})),
  ExpandedThumbnail = Table.TransformColumns(ExpandedLocation, ThumbnailChanges, null, MissingField.UseNull),
  LookupMultiTypeRows = Table.SelectRows(TableSchema, each [NativeTypeName] = "LookupMulti"),
  LookupMultiFieldNames = {"lookupId", "lookupValue", "isSecretFieldValue"},
  LookupMultiTransforms = Table.AddColumn(LookupMultiTypeRows, "LookupMultiTransform", each(name) => 
                    if (name <> "") then @Text.Combine(Table.Column(Table.FromList(name, Record.FieldValues, LookupMultiFieldNames), "lookupValue"), ", ") else null, Function.Type),
  LookupMultiChanges = Table.ToRows(Table.SelectColumns(LookupMultiTransforms, { "Name","LookupMultiTransform"})),
  ExpandedLookupMulti = Table.TransformColumns(ExpandedThumbnail, LookupMultiChanges, null, MissingField.UseNull),
  TaxonomyFieldTypeMultiTypeRows = Table.SelectRows(TableSchema, each [NativeTypeName] = "TaxonomyFieldTypeMulti"),
  TaxonomyFieldTypeMultiFieldNames = {"Label", "TermID"},
  TaxonomyFieldTypeMultiTransforms = Table.AddColumn(TaxonomyFieldTypeMultiTypeRows, "TaxonomyFieldTypeMultiTransform", each(name) => 
                    if (name <> "") then @Text.Combine(Table.Column(Table.FromList(name, Record.FieldValues, TaxonomyFieldTypeMultiFieldNames), "Label"), ", ") else null, Function.Type),
  TaxonomyFieldTypeMultiChanges = Table.ToRows(Table.SelectColumns(TaxonomyFieldTypeMultiTransforms, { "Name","TaxonomyFieldTypeMultiTransform"})),
  ExpandedTaxonomyFieldTypeMulti = Table.TransformColumns(ExpandedLookupMulti, TaxonomyFieldTypeMultiChanges, null, MissingField.UseNull),
  MultiChoiceTypeRows = Table.SelectRows(TableSchema, each [NativeTypeName] = "MultiChoice"),
  MultiChoiceTransforms = Table.AddColumn(MultiChoiceTypeRows, "MultiChoiceTransform", each(name) => 
                    if (name <> "") then @Text.Combine(name, ", ") else null, Function.Type),
  MultiChoiceChanges = Table.ToRows(Table.SelectColumns(MultiChoiceTransforms, { "Name","MultiChoiceTransform"})),
  ExpandedMultiChoice = Table.TransformColumns(ExpandedTaxonomyFieldTypeMulti, MultiChoiceChanges, null, MissingField.UseNull)
in
  ExpandedMultiChoice
```
