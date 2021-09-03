import pandas as pd
import collections

CSV_PATH = ""

Fields = collections.namedtuple("Fields", ["timestamp", "item", "cost", "income", "pay_way", "comment", "e_platform"])
fields = Fields(timestamp="Timestamp", item="item", cost="cost",
                income="income", pay_way="pay_way", comment="comment", e_platform="e-commerce platform")
AnalysisFields = collections.namedtuple("AnalysisFields", ["year", "month"])
af = AnalysisFields(year="year", month="month")


def init(df: pd.DataFrame):
    df[fields.timestamp] = pd.to_datetime(df[fields.timestamp], format="%d/%m/%Y %H:%M:%S")
    return df


def get_year_month(df: pd.DataFrame):
    df[af.year] = df[fields.timestamp].dt.year
    df[af.month] = df[fields.timestamp].dt.month
    return df


if __name__ == '__main__':
    df = pd.read_csv(CSV_PATH)
    inited_df = init(df)
    ymdf = get_year_month(inited_df)
    print("========TOTAL========")
    print(ymdf[[af.year, af.month, fields.cost]].groupby([af.year, af.month]).sum())
    print("====================")
    print("======BREAKDOWN======")
    print(ymdf[[af.year, af.month, fields.cost, fields.item]].groupby([af.year, af.month, fields.item]).sum())
    print("====================")
    print(ymdf[[af.year, af.month, fields.cost, fields.item]].groupby([af.year, af.month, fields.item]).count())

    # change the insurance to each month
    def get_shopping_part(item):
        return "Shopping" in item or "Supermarket" in item
    print(ymdf[ymdf[fields.item].apply(get_shopping_part)].groupby([af.year, af.month, fields.item]).sum())
    cnt = ymdf[ymdf[fields.item].apply(get_shopping_part)].groupby([af.year, af.month, fields.item]).count()
    print(cnt)