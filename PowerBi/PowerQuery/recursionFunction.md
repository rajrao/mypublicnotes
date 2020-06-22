Simple Example

    let
          factorial = (n as number) => let
          result = if n <= 0 then 1 else n * @factorial(n -1) 
          in result
      in
          factorial
          
          
Example showing multiple steps in recursive call


    let
          factorial = (x as number) =>
          let  
              factorialInternal = (n) =>   
              let
                  result = if n <= 0 then 1 else n * @factorialInternal(n -1) 
              in  
                  result, 
              x = x*1, 
              Results = factorialInternal(x)
          in  
              Results
      in
          factorial
