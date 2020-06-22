A basic function template showing a function definition, with sub functions

      let
          source = (x as number) =>
          let  
              x1 = (a, b) =>   
              let
                  c = a * b, 
                  x1 = c * -1 
              in  
                  x1,  
              x2 = (a, b) =>   
              let   
                  c = a+b,
                  x2 = c * 2  
              in  
                  x2,  
              a = x+1,
              b = x+2,
              Results = x1(a,b) + x2(a,b)
          in  
              Results
      in
          source
