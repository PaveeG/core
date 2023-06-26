from rtdip_sdk.pipelines.execute import PipelineJob, PipelineStep, PipelineTask, PipelineJobExecute
from rtdip_sdk.pipelines.sources.spark.weather import *
from rtdip_sdk.pipelines.destinations import SparkDeltaDestination

step_list = []
# pip install pyspark==3.2.2

# parameters = {"language": "en-US", "units": "e", "apiKey": kwargs["api_key"]}

# WeatherForecastAPIV1Source
# WeatherForecastAPIV1Source_Multi
# WeatherForecastAPIV3Source (supports Solar)

step_list.append(PipelineStep(
    name="test_step1",
    description="test_step1",
    # component=MISOHistoricalLoadISOSource,
    component=WeatherForecastAPIV1Source,
    component_parameters={"options": {
        "lat": "32.3667",
        "lon": "-95.4",
        "api_key": "25983b75239c4efd983b75239cfefd4c",
        "language": "en-US",
        # "units":"e"
        # "params": {"language": "en-US", "units": "e", "apiKey": "25983b75239c4efd983b75239cfefd4c"}
        # "load_type": "actual",
        # "date": "20230510"
    },
    },
    provide_output_to_step=["test_step3"]
))

# transform step
# step_list.append(PipelineStep(
#     name="test_step2",
#     description="test_step2",
#     component=BinaryToStringTransformer,
#     # component_parameters={
#     #     "source_column_name": "body",
#     #     "target_column_name": "body"
#     # },
#     depends_on_step=["test_step1"],
#     provide_output_to_step=["test_step3"]
# ))

# write step
step_list.append(PipelineStep(
    name="test_step3",
    description="test_step3",
    component=SparkDeltaDestination,
    component_parameters={
        "table_name": "weather_forecast_data",
        "options": {},
        "mode": "overwrite"
    },
    depends_on_step=["test_step1"]
))
task = PipelineTask(
    name="test_task",
    description="test_task",
    step_list=step_list,
    batch_task=True
)

pipeline_job = PipelineJob(
    name="test_job",
    description="test_job",
    version="0.0.1",
    task_list=[task]
)

pipeline = PipelineJobExecute(pipeline_job)

result = pipeline.run()
