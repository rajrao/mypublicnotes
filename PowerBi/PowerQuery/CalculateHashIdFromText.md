This is based on this answer: https://community.powerbi.com/t5/Desktop/Privacy-Hashing-of-keys/m-p/534546/highlight/true#M250677

Itutilizes the fact that PBI can perform compression and uses GZips.  GZip's last 8 bytes is the "footer". The first 4 of which is the CRC32 checksum
https://docs.fileformat.com/compression/gz/#gz-file-footer

Warning Crc32 can cause collisions! https://preshing.com/20110504/hash-collision-probabilities/. When I tried using it against Salesforce IDs, I got a clash with just 100k Ids.

Create a blank query and insert the following code.

```
let
    CalculateHash = (x as text) as text => 
    let
        compressedText = Binary.Compress(Text.ToBinary(x, BinaryEncoding.Base64), Compression.GZip),
        asArray = Binary.ToList(compressedText),
        last8Bytes = List.LastN(asArray,8),
        first4OfTheLast8Bytes = List.FirstN(last8Bytes,4),
        asBinary = Binary.FromList(first4OfTheLast8Bytes),
        hashId = BinaryFormat.UnsignedInteger32(asBinary),
        hashIdAsText = Number.ToText(hashId)
    in
        hashIdAsText
in
    CalculateHash
```
