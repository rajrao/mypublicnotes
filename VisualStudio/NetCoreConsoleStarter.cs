class Program
    {
        static async Task Main(string[] args)
        {
            var backgroundColor = Console.BackgroundColor;
            var foregroundColor = Console.ForegroundColor;
            Console.Clear();

            var services = new ServiceCollection();
            var argumentsHasErrors = ProcessCommandLineArgs(args, services);

            if (!argumentsHasErrors)
            {
                ConfigureServices(services);
                await using ServiceProvider serviceProvider = services.BuildServiceProvider();
                var appOptions = serviceProvider.GetService<AppOptions>();
                IApp app = serviceProvider.GetService<MyApp>();
                if (app == null)
                {
                    throw new InvalidOperationException($"Service not registered for {appOptions.GetType()}");
                }
                CancellationTokenSource source = new CancellationTokenSource();
                CancellationToken token = source.Token;
                await app.Run(token);
            }

            Console.ForegroundColor = foregroundColor;
            Console.BackgroundColor = backgroundColor;

        }

        private static bool ProcessCommandLineArgs(string[] args, ServiceCollection services)
        {
            bool argumentsHasErrors = false;
            var parserResult = new CommandLine.Parser(config =>
                {
                    config.HelpWriter = null;
                    config.CaseSensitive = false;
                    config.AutoHelp = true;
                    config.IgnoreUnknownArguments = false;
                })
                .ParseArguments<XXXX>(args); //list options classes

            parserResult
                .WithParsed(appOptions =>
                {
                    services.AddSingleton(appOptions as AppOptions);
                    Console.WriteLine(Parser.Default.FormatCommandLine(appOptions, configuration =>
                    {
                        configuration.UseEqualToken = true;
                        configuration.SkipDefault = false;
                    }));
                })
                .WithNotParsed(errors =>
                {
                    argumentsHasErrors = true;
                    var helpText = HelpText.AutoBuild(parserResult, h =>
                    {
                        h.AdditionalNewLineAfterOption = false;
                        h.AddNewLineBetweenHelpSections = true;

                        /*h.AddPreOptionsLines(new List<string>
                        {
                           "xxxx"
                        });*/
                        return HelpText.DefaultParsingErrorsHandler(parserResult, h);
                    }, e => e);
                    Console.WriteLine(helpText);
                });
            return argumentsHasErrors;
        }

        private static void ConfigureServices(ServiceCollection services)
        {
            var configuration = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("local.settings.json", false)
                .Build();
            var appSettings = configuration.GetSection("Configuration").Get<AppSettings>();
            services.AddOptions();

            services.AddLogging(configure =>
                {
                    var configurationSection = configuration.GetSection("Logging");
                    configure
                        .AddConfiguration(configurationSection)
                        .AddConsole()
                        .AddFile(configurationSection);
                })
                .AddSingleton<ServiceBusUtils>()
                .AddSingleton<IAppSettings>(appSettings)
                .AddTransient<EstateBasedRunner>()
                .AddTransient<MovieLineUpGenerator>()
                .AddTransient<UxFinanceSalesMessageRunner>()
                .AddTransient<UxFinanceDrMessageRunner>()
                .AddTransient<UxFinanceCsMessageRunner>()
                .AddTransient<AttendanceFeedGenerator>()
                .AddTransient<EstateWebApiOAuthMessageHandler>()
                .AddHttpClient<EstateWebApiOAuthMessageHandler>();

            //serviceCollection.AddSingleton<ITelemetryInitializer, DeliveryManTelemetryInitializer>();
            //var instrumentationKey = Configuration["ApplicationInsights:InstrumentationKey"];
            //serviceCollection.AddApplicationInsightsTelemetryWorkerService(instrumentationKey);
            //serviceCollection.Configure<ApplicationInsightsLoggerOptions>(config => config.FlushOnDispose = true);


            services.AddHttpClient<IEstateHttpClient, EstateHttpClient>()
                .AddHttpMessageHandler<EstateWebApiOAuthMessageHandler>();
            services.AddMemoryCache();
        }
    }
    
    
/*
config file
{
  "Configuration": {
    "AppSetting1": "Blah",
    
  },
  "Logging": {
    "ApplicationInsights": {
      "LogLevel": {
        "NamespaceNameHere": "Information"
      }
    },
    "LogLevel": {
      "Default": "Information",
      "System": "Warning",
      "Microsoft": "Warning",
      "Microsoft.Hosting.Lifetime": "Information"
    },
    "File": {
      "Path": "C:\\Tools\\AADataGenerator\\app.log",
      "Append": "True",
      "FileSizeLimitBytes": 0, // use to activate rolling file behaviour
      "MaxRollingFiles": 0 // use to specify max number of log files
    }
  },
  "ApplicationInsights": {
    "InstrumentationKey": "xxxxx"
  }
}
*/
