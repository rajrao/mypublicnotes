This depends upon a cross join table between the locations that you need to compute the distance. One simple way to do this is to create a copy of your locations table and then join them on a field like Country.

    Distance = 
    var curLat = min(Locations[Latitude])
    var curLon = min(Locations[Longitude])
    var otherLat = Min(LocationsOther[Latitude])
    var otherLon = Min(LocationsOther[Longitude])
    var latDiff = Abs(curLat - otherLat)
    var lonDiff = Abs(curLon - otherLon)
    --0.017453: deg2Rad, 7917.5: earth dia
    --return if (latDiff> 0 && lonDiff > 0, ASIN((SQRT(0.5 - COS((otherLat-curLat) * 0.017453)/2 + COS(curLat * 0.017453) * COS(otherLat * 0.017453) * (1-COS((otherLon- curLon) * 0.017453))/2))) * 7917.5) 
    return if (latDiff> 0 && lonDiff > 0, ASIN((SQRT(0.5 - COS(latDiff * 0.017453)/2 + COS(curLat * 0.017453) * COS(otherLat * 0.017453) * (1-COS(lonDiff * 0.017453))/2))) * 7917.5) 
