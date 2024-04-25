from typing import List
from uuid import UUID
import pytest
from store.usecases.product import product_usecase
from store.schemas.product import ProductOut, ProductUpdateOut
from store.core.exceptions import BaseException, NotFoundException
from tests.conftest import product_up

async def test_usecases_shoud_return_success(product_in):
    result = await product_usecase.create(body=product_in)
    
    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 pro Max"
    
async def test_usecases_get_shoud_return_success(product_inserted):
    result = await product_usecase.get(id=product_inserted.id)
    
    assert result is not None
    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 pro Max"
    
async def test_usecases_get_shoud_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.get(id=UUID('c9e99e2c-09b1-4fc8-97c1-2883e128f09b'))
    
    assert err.value.message == "Product not found with filter: c9e99e2c-09b1-4fc8-97c1-2883e128f09b"

@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_shoud_return_success():
    result = await product_usecase.query()
    assert result is not None
    assert isinstance(result, List)
    assert len(result) > 1
    
async def test_usecases_update_shoud_return_success(product_up, product_inserted):
    product_up.price = 7.500
    result = await product_usecase.update(id=product_inserted.id, body=product_up)
    assert isinstance(result, ProductUpdateOut)

async def test_usecases_delete_shoud_return_success(product_inserted):
    result = await product_usecase.delete(id=product_inserted.id)
    assert result is True
    
async def test_usecases_delete_shoud_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.delete(id=UUID('c9e99e2c-09b1-4fc8-97c1-2883e128f09b'))
    
    assert err.value.message == "Product not found with filter: c9e99e2c-09b1-4fc8-97c1-2883e128f09b"