# Sample Predictions with Certainty

## Example 1
**Text:**
```
N34 N14 N01 APIN~a PA~a AN MAR~a
N34 N45 N14 N01 PA~a SZUBUR
N46 N19 N04 PA~a SZUBUR
N34 E2~a DU SZE~a
N45 N14 EN~a PAP~a
N34 N14 N01 BU~a RAD~a
N46 N19 N04
N45 N14 N01 SZE~a MUSZEN KASZ~c
N34 N14 N01 SZE~a BA
N46 N19 N04
N34 N36 N14 N01 SZE~a GIBIL BA AN MAR~a EN~a A SZAM2
```
**True Labels:** ['cereals']
**Predicted Labels:** ['cereals']
**Certainty:** [0.99]

## Example 2
**Text:**
```
MUSZEN NA~a GI
N14 N57 SZU
N01 GAR
N14 MUSZEN NA~a GI
N14 N22 N01 N57 SZU
MUSZEN NA~a GI
N14 N57 SZU
N50 N14 UB ZI~a
N14 SZE~a+SAR
N14 UB E2~a GAL~a
```
**True Labels:** ['fields']
**Predicted Labels:** ['cereals', 'fields']
**Certainty:** [0.57, 0.83]

## Example 3
**Text:**
```
N19 NUMUN APIN~a
N01 N39~a NINDA2xX
KID~b DU APIN~a GI4~a
N34x1N58 SUR
```
**True Labels:** ['cereals']
**Predicted Labels:** ['cereals']
**Certainty:** [0.93]

## Example 4
**Text:**
```
N14 N01 LAL2~a BULUG3
N14 N01 ZI~a
N01 LAL2~a APIN~a GI
N14 KI N57 BULUG3
BA KALAM~g A AN MAR~a PA~a
GAN2 SI EN~a ISZ~a
AB~a GIBIL 
N14 N01 GAN2
N34 N14 N01
KALAM~g E2~a NUN~a A MAR~a NU11 BULUG3
```
**True Labels:** ['fields']
**Predicted Labels:** ['cereals']
**Certainty:** [0.57]

## Example 5
**Text:**
```
N01 DUG~c DUB~a
N01 ZABALAM~a AN BA ZATU751~a
N01 SAL BA ANSZE~b
N01 BA KI
N01
N01 KU3~a
ZATU649
N01 KU3~a ZABALAM~a AB2
N01 SI4~a NE~a SZE~a GI
GA~a
N01 ZATU648
N57.PIRIG~b1 AB~b SU~a
N01 SI U4 AB2
N01 TUR3~a A
GA~a BU~a HI
N01 ZATU648
N01 SI U4 AB2
N01 TUR3~a A
N01
N01 KU3~a
ZATU649
N01 KU3~a ZABALAM~a AB2
N01 NE~a SI4~a GI SZE~a
N14 N01 ZATU648 DUG~c GI&GI BA
```
**True Labels:** ['dairy']
**Predicted Labels:** ['dairy']
**Certainty:** [1.0]

## Example 6
**Text:**
```
SI4~a SIG NE~a SZE~a GI
N34 U2~a
N34 N14 U2~a
N34 N14 SUHUR
NAGAR~b NANSZE~a
N34 N14 N01
```
**True Labels:** ['fish']
**Predicted Labels:** ['fish']
**Certainty:** [1.0]

## Example 7
**Text:**
```
N45 N14 U4x1N57 SZE~a NE~a DA~a SZA3~a2 ZATU757
EN~a SZU
N19
N14 HIx1N57 GI6
N45 N14 U4x2N57 SZE~a SZA3~a2 ZATU756 GAN2
N45 N14 U4x3N57 
N14 ZATU756
N14
N14 U4x4N57
N14 U4x5N57 SZE~a EN~a KI ME~a UR2 RAD~a KU6~a
N14 U4x6N57 SZUBUR AB2
N14 N19 U4x7N57 MAR~a MUSZEN ZATU756
N45 N14 U4x8N57 SZE~a
N34 N45 U4x8N57 SZE~a SAL.SZU2 KU6~a GU7
```
**True Labels:** ['cereals']
**Predicted Labels:** ['cereals']
**Certainty:** [0.99]

## Example 8
**Text:**
```
N14
N14 AN NAMESZDA
N19
N14 EN~a SZE~a NE~a
N19
UB
N19
```
**True Labels:** ['cereals']
**Predicted Labels:** ['cereals']
**Certainty:** [1.0]

## Example 9
**Text:**
```
N34 SANGA~a KISZ
N01 EN~a TUG2~a
N01 KISZ SZUBUR
SANGA~a
N14 EN~a AMAR
N01 AN SZU2.EN~a
N14 N01 KAB NAM2
N01 KAB NAM2 SZE~a.NAM2
N01 MAR~a
N01 GAN2
N01 ZATU703 GAL~a SANGA~a
SANGA~a
N34 NAMESZDA RU
N14 NAGA~a
N14 N01 UB
N34 SANGA~a KISZ BA
N14
BA
N34 N14 N01 UB SZU
N14 KISZ
N01 EN~a+NUN~b SANGA~a
N34 N14 N01 BA
N34 N14 N01 SZU
N14
N34 N14 N01 BA KISZ
```
**True Labels:** ['animals']
**Predicted Labels:** ['animals', 'textiles']
**Certainty:** [0.69, 0.83]

## Example 10
**Text:**
```
HAL
N30~a KASZ~b ZATU714xHI@g~a MU
N01 U2~a DU6~b
N01 U4 SAL HAL
N14 TUR HAL SAL
N01 EN~a TU~b GISZxSZU2~a
N14 N01 SZITA~a1 NAMESZDA 
N01 N57 GAL~a
N01
```
**True Labels:** ['cereals']
**Predicted Labels:** ['cereals']
**Certainty:** [0.83]

## Example 11
**Text:**
```
N01 AN NU11 
N01 EN~a
N01 N04 NUMUN
N01 SIG2~a N19 SZE~a
AN SZA3~a1 UR2
N01 KU3~a A GISZ3~a
N01 NU11 AN 
N22 KASZ~a GUG2 BAR
SANGA~a SI KISAL~b1 GAL~a
N01 NU11 AN 
N01 SANGA~a DUB~a
N01 EN~a GA2~a1 ME~a DU SZU
N01 TUR3~a N57
N01 ME~a DAR~b PAP~a
 BA 
AL
```
**True Labels:** ['cereals']
**Predicted Labels:** ['cereals']
**Certainty:** [0.6]

## Example 12
**Text:**
```
N48 N34 N14 N01 N57.DU6~a@n
N34 N14 IDIGNA ZATU741
N14 KISAL~b1
N14 N01 GI
N01 PA~a
N01 RU
N01 MUSEN
N01 E2~a
N01 
UBI~c
N48 N01 UBI~c
```
**True Labels:** ['fish']
**Predicted Labels:** []
**Certainty:** []

## Example 13
**Text:**
```
N14 NAR SZE~a
N14 SZE~a EN~a A
N14 SZE~a NAR
SZE~a PAP~a
N01 UD5~a
N01 PA~a
N01 ZATU710 GI
N01 SZU SAL PAP~a
N01 AB2 GI4~a
N01 GU4@g BAR
N01 PAP~a SZE~a
N14 N01 SZE~a SZU
```
**True Labels:** ['cereals']
**Predicted Labels:** ['animals', 'cereals']
**Certainty:** [0.6, 0.96]

## Example 14
**Text:**
```
N45
N14 TAR~a
SANGA~a SZITA@g~ax1N06
N14
N01 TAR~a
ME~a NI~a.RU
N14
N01 TAR~a
SANGA~a NI~a.RU
SZE~a GU7
N45 N14 SZE~a GU7
```
**True Labels:** ['cereals']
**Predicted Labels:** ['cereals']
**Certainty:** [1.0]

## Example 15
**Text:**
```
N01 ZATU850
N01 SZA3~b1
N01 U2~a
N01 EN~a+NUN~b
N01 SUKKAL
N01 EN~a KI
N01 KU~a SZE~a@t
N01 SI A
N01 EN~a 
N01 SI AD~a
N01 KAB SZUBUR
N01 N57 PAP~a
N01 SI GI
N14 SANGA~a
N01 AMAR
N01 ZATU703
N01 DU
N01 SZEG9
N01 E~b EN~a+NUN~b
N01 APIN~a GUG2
N14 N01 KISZ PAP~a GI N02
```
**True Labels:** ['animals']
**Predicted Labels:** ['animals']
**Certainty:** [0.96]

## Example 16
**Text:**
```
N20 N05 N42~a NAR SZE~a
N14 N01 N39~a E2~b SZE~a BU~a
N05 BA AL DU
NAR A
N14
N20 N05 SZE~a BAR
N20 N05 SZE~a
AL BA
N14 N01 N39~a NAR A
N14 N01 SZE~a BA AL DU
SAG
```
**True Labels:** ['cereals']
**Predicted Labels:** ['cereals']
**Certainty:** [1.0]

## Example 17
**Text:**
```
N14 N01 KISZ SUKKAL RAD~a
N14 N01 DUB~a
N14 NAGAR~a
N14 N01 ERIM~a
```
**True Labels:** ['animals']
**Predicted Labels:** []
**Certainty:** []

## Example 18
**Text:**
```
N14 N01 SZE~a ERIM~a
N14 N01 NI~a SZE~a 
N14 N01 RU 
N14 N01 A AB~a 
N01 
N14 N01 EN~a DU 
N14 N08 
N01 N08
N14 N01
N19
N14 SZITA~a1 E2~a 
SZUBUR TE 
N14 N58 N14 N01 N08 SZE~a
N19 N08~b TE
N14 N58 N14 N01 SZE~a
```
**True Labels:** ['cereals']
**Predicted Labels:** ['cereals']
**Certainty:** [0.96]

## Example 19
**Text:**
```
SZE~a BA
N01 GAN2 RU UR2 URU~a1
N01 UDU~a HI
N57 SZU2 ZAG~a
N14 SZE~a&SZE~a DU GI6 IB~a
N14 SZU2 PAP~a SAL APIN~a
KID~c PAP~a APIN~a
N01 EN~a DU GISZ SUHUR GI GISZ3~a PA~a KU3~a A 
N01 EN~a A DU TUR
```
**True Labels:** ['cereals']
**Predicted Labels:** []
**Certainty:** []

## Example 20
**Text:**
```
N19 N04 AN SZU2.EN~a SZITA~a1
N19 SZE~a&SZE~a ZATU773~b IB~a
N04 SAL ZATU751~b BU~a
N04 DIM~a EN~a
N04 PAP~a
N04 SAG 
N41 NE~a SAL
N41 U4 AN SAL
N41 GI6 SAL
N04 AN AMA~a GI
N04 
N04 U4 
N19 N04 N41
```
**True Labels:** ['cereals']
**Predicted Labels:** ['cereals']
**Certainty:** [0.99]

## Example 21
**Text:**
```
N45 N14 N01 SZE~a
N46 N19 KA~a NAM~d
SZU&SZU
EN~a SZU
 PAP~a
N36 N19 SZE~a
N04 AN SAG
NAM2
```
**True Labels:** ['cereals']
**Predicted Labels:** ['cereals']
**Certainty:** [1.0]

## Example 22
**Text:**
```
N34 N14 N01 UDU~a
AN SZE~a@t NI~a
N34 N01 IDIGNA GAL~a SANGA~a
N34 N14 DI RAD~a
N01 URI3~a IB~a
N01 AN UR5~a NAM2 DI
N01 SANGA~a GAL~a AN UR5~a
```
**True Labels:** ['animals']
**Predicted Labels:** []
**Certainty:** []

## Example 23
**Text:**
```
N01 EN~a ASAR
N02
N14 ZATU703
N02
N14 N01 KI
N02 BA
N02
N01 
N14 N01 
N02 BA
N01 E2~a KUR~a
N02 MAH~a
N01 SUKKAL
N02
N14 UR4~a
N01 RU
N02
GAL~a 
EN~a
N14 N01 ZATU759 SAG
N01 SI
N02
N01 E2~a NU@g
N14 N01 ZATU703 BA EN~a
N01 SANGA~a AN EN~a RU
N02 NE~a
N01 EN~a
N01 SUKKAL URU~a1 GISZ RAD~a
N01 EN~a SZU ESZDA
N02
N02 NE~a
KISZ GAL~a
N34 N14 MUN~a1 BA
N02 BA
N15 N02
N02 NE~a
N34 N14 N01 MUN~a1
```
**True Labels:** ['animals']
**Predicted Labels:** []
**Certainty:** []

## Example 24
**Text:**
```
N01 
N01 GAN2
N01
N01 GURUSZDA~a UDU~a
N01 SANGA~a
N01 EN~a KI
N01 ZATU628~a
UDU~a BAR
N14 N01 UDU~a BAR
```
**True Labels:** ['animals']
**Predicted Labels:** ['animals']
**Certainty:** [0.99]

## Example 25
**Text:**
```
N14 N01 SZE~a RU
N01 RU
N14 N01 SZE~a RU
N14 SZUBUR ADAB
N14 ZATU710 
N14 
N01
N01 A TAK4~a
N01 UMUN2 DU
N01 URI3~a AN
N04 U4 NIM~b1
N14 AN MAR~a PA~a
N14 NAB DI
N45 N14 N01 SZE~a EN~a APIN~a
N14 N01 E2~b
N04
N45 N14 N01 N39~a N24
```
**True Labels:** ['cereals']
**Predicted Labels:** ['cereals']
**Certainty:** [0.99]

