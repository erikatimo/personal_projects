"""
    Created at: 2022-04-03
    Author: Erika Timo de Oliveira
    Description: Data Envelopment Analysis implementation
"""




if __name__ == "__main__":
    X = np.array([
        [20., 300.],
        [30., 200.],
        [40., 100.],
        [20., 200.],
        [10., 400.]
    ])
    y = np.array([
        [1000.],
        [1000.],
        [1000.],
        [1000.],
        [1000.]
    ])
    names = [
        'Bratislava',
        'Zilina',
        'Kosice',
        'Presov',
        'Poprad'
    ]
    dea = DEA(X,y)
    dea.name_units(names)
    dea.fit()
    print(dea.output_w)
    print(dea.input_w)
    print(dea.lambdas)
    print(dea.efficiency)