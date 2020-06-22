A basic function template showing a function definition, with sub functions

      let
          source = (x as number) =>
          let  
              x1 = (a, b) =>   
                  let   
                  c = a*b  
                  in  
                      c,  
              x2 = (a, b) =>   
                  let   
                  c = a+b  
                  in  
                      c,  
              a = x *100,
              b = x *1000,
              Results = x1(a,b) + x2(a,b)
          in  
              Results
      in
          source
