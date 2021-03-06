import pytest
import numpy as np
import scipy
from sklearn.datasets import load_boston
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge as BaselineRidgeRegression
from bbai.glm import RidgeRegression

@pytest.fixture
def boston_dataset():
    X, y = load_boston(return_X_y=True)
    X = StandardScaler().fit_transform(X)
    return X, y

def test_aloocv_optimization(boston_dataset):
    X, y = boston_dataset
    model = RidgeRegression(tolerance=1.0e-6)
    model.fit(X, y)
    assert model.alpha_ == pytest.approx(4.680170622758263)

def test_against_baseline(boston_dataset):
    X, y = boston_dataset
    alpha = 1.0
    model = RidgeRegression(tolerance=1.0e-6, alpha=alpha)
    model.fit(X, y)
    assert model.alpha_ == pytest.approx(alpha)
    
    model_p = BaselineRidgeRegression(alpha=alpha, tol=1.0e-6)
    model_p.fit(X, y)

    np.testing.assert_array_almost_equal(model.coef_, model_p.coef_, decimal=3)
    np.testing.assert_array_almost_equal(model.intercept_, model_p.intercept_, decimal=3)

    pred = model.predict(X)
    pred_p = model_p.predict(X)
    np.testing.assert_almost_equal(pred, pred_p)

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
