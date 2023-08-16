from multiprocessing import Value

import synthesized
from synthesized import HighDimSynthesizer, MetaExtractor, ConditionalSampler
from synthesized.common.rules import Association, ValueRange, Column, Value, IsIn
from synthesized.privacy import MaskingFactory
from synthesized.metadata.value import Person, Address
from synthesized.config import PersonLabels, PersonModelConfig, AddressLabels
import pandas as pd
from faker import Faker

SYNTHETIC_FOLDER = ''
DATA_FILE = f'{SYNTHETIC_FOLDER}customer-data'

if __name__ == '__main__':
    customer = pd.read_csv(filepath_or_buffer=f'{DATA_FILE}.csv')

    # data privacy - paid version required !!!
    # person = Person(
    #     name='person',
    #     labels=PersonLabels(
    #         gender='SEX',
    #         firstname='FNAME',
    #         lastname='LNM',
    #         email='EMAIL'
    #     )
    # )

    # permanent_address = Address(
    #     name='permanent_address',
    #     labels=AddressLabels(
    #         postcode='PZIP',
    #         county='PCNTRY',
    #         city='PCITY',
    #         district='PSTATE',
    #         street='PAD1',
    #         house_number='PAD2'
    #     )
    # )

    # mail_address = Address(
    #     name='mail_address',
    #     labels=AddressLabels(
    #         postcode='MZIP',
    #         county='MCNTRY',
    #         city='MCITY',
    #         district='MSTATE',
    #         street='MAD1',
    #         house_number='MAD2'
    #     )
    # )

    # paid version required !!!
    # annotations = [person, mail_address, permanent_address]

    # metadata extraction
    # df_meta = MetaExtractor.extract(df=customer, annotations=annotations)
    df_meta = MetaExtractor.extract(df=customer)

    # initialize model
    synth = HighDimSynthesizer(df_meta)

    # learning process
    synth.learn(customer)

    # model export:
    # with open("customer-model.synth", "wb") as file_handle:
    #     HighDimSynthesizer.export_model(file_handle)

    # new data generation
    # new_data = synth.synthesize(num_rows=100, association_rules=[pers_sex_rule], generic_rules=[branch_range_rule])

    # column rules
    pers_sex_rule = Association.detect_association(customer, df_meta, associations=["PERS", "SEX"])
    # branch limit from 0 to 9999
    # values = [Value(0), Value(9999)]
    # branch_range_rule = ValueRange(v1=Column("BOO"), v2=values)
    values = [Value(i) for i in range(10000)]
    branch_range_rule = IsIn(Column("BOO"), values)

    conditional_sampler = ConditionalSampler(synthesizer=synth)
    new_data = conditional_sampler.synthesize(num_rows=100, association_rules=[pers_sex_rule])
    # new_data = conditional_sampler.synthesize(num_rows=100, generic_rules=[branch_range_rule])
    new_data.to_csv(f'{DATA_FILE}-new.csv')

    print("Process finished with new (artificial) data:")
    print(new_data.loc[:])

    # for table in new_data:
    #     print(table)
    #     data_frame = pd.DataFrame(new_data[table])
    #     print(data_frame)
