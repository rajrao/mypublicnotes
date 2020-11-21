This depends upon a cross join table between the locations that you need to compute the distance. One simple way to do this is to create a copy of your locations table and then join them on a field like Country.

    Distance =
        VAR curLat =
            MIN ( Sites[Latitude] )
        VAR curLon =
            MIN ( Sites[Longitude] )
        VAR otherLat =
            MIN ( SiteCopy[Latitude] )
        VAR otherLon =
            MIN ( SiteCopy[Longitude] )
        VAR latDiff =
            ABS ( curLat - otherLat )
        VAR lonDiff =
            ABS ( curLon - otherLon ) --0.017453: deg2Rad, 7917.5: earth dia
        RETURN
            IF (
                latDiff > 0
                    && lonDiff > 0,
                ASIN (
                     (
                        SQRT (
                            0.5
                                - COS ( latDiff * 0.017453 ) / 2
                                + COS ( curLat * 0.017453 )
                                    * COS ( otherLat * 0.017453 )
                                    * (
                                        1
                                            - COS ( lonDiff * 0.017453 )
                                    ) / 2
                        )
                    )
                ) * 7917.5
            )
