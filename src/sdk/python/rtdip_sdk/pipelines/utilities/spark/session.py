# Copyright 2022 RTDIP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import sys
import inspect
from typing import List
from pyspark.sql import SparkSession

from ..interfaces import UtilitiesInterface
from ..._pipeline_utils.models import Libraries, SystemType
from ..._pipeline_utils.spark import SparkClient

class SparkSessionUtility(UtilitiesInterface):
    '''
    Creates or Gets a Spark Session and uses settings and libraries of the imported RTDIP components to populate the spark configuration and jars in the spark session.

    Call this component after all imports of the RTDIP components to ensure that the spark session is configured correctly. 

    Args:
        config (dict): Dictionary of spark configuration to be applied to the spark session
        module (optional str): Provide the module to use for imports of rtdip-sdk components. If not populated, it will use the calling module to check for imports
    ''' 
    spark: SparkSession
    config: dict
    module: str

    def __init__(self, config: dict, module:str = None) -> None:
        self.config = config
        if module == None:
            frm = inspect.stack()[1]
            mod = inspect.getmodule(frm[0])
            self.module = mod.__name__
        else:
            self.module = module

    @staticmethod
    def system_type():
        '''
        Attributes:
            SystemType (Environment): Requires PYSPARK
        '''            
        return SystemType.PYSPARK

    @staticmethod
    def libraries():
        libraries = Libraries()
        return libraries
    
    @staticmethod
    def settings() -> dict:
        return {}

    def execute(self) -> SparkSession:
        from ...sources.interfaces import SourceInterface
        from ...destinations.interfaces import DestinationInterface
        from ...deploy.interfaces import DeployInterface
        from ...secrets.interfaces import SecretsInterface
        from ...transformers.interfaces import TransformerInterface
        try:
            classes_imported = inspect.getmembers(sys.modules[self.module], inspect.isclass)
            component_list = []
            for cls in classes_imported:
                class_check = getattr(sys.modules[self.module], cls[0])
                if ((issubclass(class_check, SourceInterface) and class_check != SourceInterface) or
                    (issubclass(class_check, DestinationInterface) and class_check != DestinationInterface) or
                    (issubclass(class_check, DeployInterface) and class_check != DeployInterface) or
                    (issubclass(class_check, SecretsInterface) and class_check != SecretsInterface) or
                    (issubclass(class_check, TransformerInterface) and class_check != TransformerInterface) or
                    (issubclass(class_check, UtilitiesInterface) and class_check != UtilitiesInterface)
                ):
                    component_list.append(cls[1])
                    print(cls[0])

            task_libraries = Libraries()
            task_libraries.get_libraries_from_components(component_list)
            spark_configuration = {}
            for component in component_list:
                spark_configuration = {**spark_configuration, **component.settings()}
            self.spark = SparkClient(spark_configuration=spark_configuration, spark_libraries=task_libraries, spark_remote=None).spark_session
            return self.spark
        
        except Exception as e:
            logging.exception(str(e))
            raise e