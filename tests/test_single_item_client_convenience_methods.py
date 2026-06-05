import pytest
from nisystemlink.clients.assetmanagement import AssetManagementClient
from nisystemlink.clients.assetmanagement import models as asset_models
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.product import models as product_models
from nisystemlink.clients.product import ProductClient
from nisystemlink.clients.spec import models as spec_models
from nisystemlink.clients.spec import SpecClient
from nisystemlink.clients.test_plan import models as test_plan_models
from nisystemlink.clients.test_plan import TestPlanClient
from nisystemlink.clients.testmonitor import models as testmonitor_models
from nisystemlink.clients.testmonitor import TestMonitorClient
from nisystemlink.clients.work_item import models as work_item_models
from nisystemlink.clients.work_item import WorkItemClient


class TestProductClientSingleItemConvenience:
    def test__create_product__wraps_bulk_create(self):
        request = product_models.CreateProductRequest(part_number="part-number")
        created_product = product_models.Product.model_construct(id="product-id")
        captured_products = []
        client = object.__new__(ProductClient)

        def fake_create_products(products):
            captured_products.append(products)
            return product_models.CreateProductsPartialSuccess(
                products=[created_product]
            )

        setattr(client, "create_products", fake_create_products)

        response = client.create_product(request)

        assert response == created_product
        assert captured_products == [[request]]

    def test__update_product__wraps_bulk_update(self):
        request = product_models.UpdateProductRequest(id="product-id")
        updated_product = product_models.Product.model_construct(id="product-id")
        captured_calls = []
        client = object.__new__(ProductClient)

        def fake_update_products(products, replace=False):
            captured_calls.append((products, replace))
            return product_models.CreateProductsPartialSuccess(
                products=[updated_product]
            )

        setattr(client, "update_products", fake_update_products)

        response = client.update_product(request, replace=True)

        assert response == updated_product
        assert captured_calls == [([request], True)]


class TestSpecClientSingleItemConvenience:
    def test__create_spec__wraps_bulk_create(self):
        request = spec_models.CreateSpecificationsRequestObject.model_construct(
            product_id="product-id",
            spec_id="spec-id",
        )
        created_spec = spec_models.CreatedSpecification.model_construct(id="spec-id")
        captured_requests = []
        client = object.__new__(SpecClient)

        def fake_create_specs(specs):
            captured_requests.append(specs)
            return spec_models.CreateSpecificationsPartialSuccess(
                created_specs=[created_spec]
            )

        setattr(client, "create_specs", fake_create_specs)

        response = client.create_spec(request)

        assert response == created_spec
        assert captured_requests[0].specs == [request]

    def test__update_spec__wraps_bulk_update(self):
        request = spec_models.UpdateSpecificationsRequestObject.model_construct(
            id="spec-id",
            product_id="product-id",
            spec_id="spec-id",
        )
        updated_spec = spec_models.UpdatedSpecification.model_construct(id="spec-id")
        captured_requests = []
        client = object.__new__(SpecClient)

        def fake_update_specs(specs):
            captured_requests.append(specs)
            return spec_models.UpdateSpecificationsPartialSuccess(
                updated_specs=[updated_spec]
            )

        setattr(client, "update_specs", fake_update_specs)

        response = client.update_spec(request)

        assert response == updated_spec
        assert captured_requests[0].specs == [request]

    def test__update_spec__raises_on_missing_success_payload(self):
        request = spec_models.UpdateSpecificationsRequestObject.model_construct(
            id="spec-id",
            product_id="product-id",
            spec_id="spec-id",
        )
        client = object.__new__(SpecClient)

        def fake_update_specs(_specs):
            return None

        setattr(client, "update_specs", fake_update_specs)

        with pytest.raises(
            ApiException, match="Server returned no updated specs"
        ) as exc_info:
            client.update_spec(request)

        assert exc_info.value.response_data is None


class TestAssetManagementClientSingleItemConvenience:
    def test__create_asset__wraps_bulk_create(self):
        request = asset_models.CreateAssetRequest.model_construct(
            location=asset_models.AssetLocationForCreate.model_construct()
        )
        created_asset = asset_models.Asset.model_construct(id="asset-id")
        captured_assets = []
        client = object.__new__(AssetManagementClient)

        def fake_create_assets(assets):
            captured_assets.append(assets)
            return asset_models.CreateAssetsPartialSuccessResponse(
                assets=[created_asset]
            )

        setattr(client, "create_assets", fake_create_assets)

        response = client.create_asset(request)

        assert response == created_asset
        assert captured_assets == [[request]]


class TestTestPlanClientSingleItemConvenience:
    def test__create_test_plan__wraps_bulk_create(self):
        request = test_plan_models.CreateTestPlanRequest(name="test-plan")
        created_test_plan = test_plan_models.TestPlan.model_construct(id="test-plan-id")
        captured_test_plans = []
        client = object.__new__(TestPlanClient)

        def fake_create_test_plans(test_plans):
            captured_test_plans.append(test_plans)
            return test_plan_models.CreateTestPlansPartialSuccessResponse(
                created_test_plans=[created_test_plan]
            )

        setattr(client, "create_test_plans", fake_create_test_plans)

        response = client.create_test_plan(request)

        assert response == created_test_plan
        assert captured_test_plans == [[request]]

    def test__update_test_plan__wraps_bulk_update(self):
        request = test_plan_models.UpdateTestPlanRequest(id="test-plan-id")
        updated_test_plan = test_plan_models.TestPlan.model_construct(id="test-plan-id")
        captured_requests = []
        client = object.__new__(TestPlanClient)

        def fake_update_test_plans(update_request):
            captured_requests.append(update_request)
            return test_plan_models.UpdateTestPlansResponse(
                updated_test_plans=[updated_test_plan]
            )

        setattr(client, "update_test_plans", fake_update_test_plans)

        response = client.update_test_plan(request, replace=True)

        assert response == updated_test_plan
        assert captured_requests[0].test_plans == [request]
        assert captured_requests[0].replace is True

    def test__schedule_test_plan__wraps_bulk_schedule(self):
        request = test_plan_models.ScheduleTestPlanRequest(id="test-plan-id")
        scheduled_test_plan = test_plan_models.TestPlan.model_construct(
            id="test-plan-id"
        )
        captured_requests = []
        client = object.__new__(TestPlanClient)

        def fake_schedule_test_plans(schedule_request):
            captured_requests.append(schedule_request)
            return test_plan_models.ScheduleTestPlansResponse(
                scheduled_test_plans=[scheduled_test_plan]
            )

        setattr(client, "schedule_test_plans", fake_schedule_test_plans)

        response = client.schedule_test_plan(request, replace=True)

        assert response == scheduled_test_plan
        assert captured_requests[0].test_plans == [request]
        assert captured_requests[0].replace is True

    def test__create_test_plan_template__wraps_bulk_create(self):
        request = test_plan_models.CreateTestPlanTemplateRequest.model_construct(
            name="template",
            template_group="group",
        )
        created_template = test_plan_models.TestPlanTemplate.model_construct(
            id="template-id"
        )
        captured_templates = []
        client = object.__new__(TestPlanClient)

        def fake_create_test_plan_templates(test_plan_templates):
            captured_templates.append(test_plan_templates)
            return test_plan_models.CreateTestPlanTemplatePartialSuccessResponse(
                created_test_plan_templates=[created_template]
            )

        setattr(client, "create_test_plan_templates", fake_create_test_plan_templates)

        response = client.create_test_plan_template(request)

        assert response == created_template
        assert captured_templates == [[request]]


class TestWorkItemClientSingleItemConvenience:
    def test__create_work_item__wraps_bulk_create(self):
        request = work_item_models.CreateWorkItemRequest(name="work-item")
        created_work_item = work_item_models.WorkItem.model_construct(id="work-item-id")
        captured_work_items = []
        client = object.__new__(WorkItemClient)

        def fake_create_work_items(work_items):
            captured_work_items.append(work_items)
            return work_item_models.CreateWorkItemsPartialSuccessResponse(
                created_work_items=[created_work_item]
            )

        setattr(client, "create_work_items", fake_create_work_items)

        response = client.create_work_item(request)

        assert response == created_work_item
        assert captured_work_items == [[request]]

    def test__update_work_item__wraps_bulk_update(self):
        request = work_item_models.UpdateWorkItemRequest(id="work-item-id")
        updated_work_item = work_item_models.WorkItem.model_construct(id="work-item-id")
        captured_requests = []
        client = object.__new__(WorkItemClient)

        def fake_update_work_items(update_work_items):
            captured_requests.append(update_work_items)
            return work_item_models.UpdateWorkItemsPartialSuccessResponse(
                updated_work_items=[updated_work_item]
            )

        setattr(client, "update_work_items", fake_update_work_items)

        response = client.update_work_item(request, replace=True)

        assert response == updated_work_item
        assert captured_requests[0].work_items == [request]
        assert captured_requests[0].replace is True

    def test__schedule_work_item__wraps_bulk_schedule(self):
        request = work_item_models.ScheduleWorkItemRequest(id="work-item-id")
        scheduled_work_item = work_item_models.WorkItem.model_construct(
            id="work-item-id"
        )
        captured_requests = []
        client = object.__new__(WorkItemClient)

        def fake_schedule_work_items(schedule_work_items):
            captured_requests.append(schedule_work_items)
            return work_item_models.ScheduleWorkItemsPartialSuccessResponse(
                scheduled_work_items=[scheduled_work_item]
            )

        setattr(client, "schedule_work_items", fake_schedule_work_items)

        response = client.schedule_work_item(request, replace=True)

        assert response == scheduled_work_item
        assert captured_requests[0].work_items == [request]
        assert captured_requests[0].replace is True

    def test__create_work_item_template__wraps_bulk_create(self):
        request = work_item_models.CreateWorkItemTemplateRequest(
            name="template",
            template_group="group",
            type="type",
        )
        created_template = work_item_models.WorkItemTemplate.model_construct(
            id="template-id"
        )
        captured_templates = []
        client = object.__new__(WorkItemClient)

        def fake_create_work_item_templates(work_item_templates):
            captured_templates.append(work_item_templates)
            return work_item_models.CreateWorkItemTemplatesPartialSuccessResponse(
                created_work_item_templates=[created_template]
            )

        setattr(client, "create_work_item_templates", fake_create_work_item_templates)

        response = client.create_work_item_template(request)

        assert response == created_template
        assert captured_templates == [[request]]

    def test__update_work_item_template__wraps_bulk_update(self):
        request = work_item_models.UpdateWorkItemTemplateRequest(id="template-id")
        updated_template = work_item_models.WorkItemTemplate.model_construct(
            id="template-id"
        )
        captured_requests = []
        client = object.__new__(WorkItemClient)

        def fake_update_work_item_templates(update_work_item_templates):
            captured_requests.append(update_work_item_templates)
            return work_item_models.UpdateWorkItemTemplatesPartialSuccessResponse(
                updated_work_item_templates=[updated_template]
            )

        setattr(client, "update_work_item_templates", fake_update_work_item_templates)

        response = client.update_work_item_template(request, replace=True)

        assert response == updated_template
        assert captured_requests[0].work_item_templates == [request]
        assert captured_requests[0].replace is True


class TestTestMonitorClientSingleItemConvenience:
    def test__update_result__wraps_bulk_update(self):
        request = testmonitor_models.UpdateResultRequest(id="result-id")
        updated_result = testmonitor_models.Result.model_construct(id="result-id")
        captured_calls = []
        client = object.__new__(TestMonitorClient)

        def fake_update_results(results, replace=False):
            captured_calls.append((results, replace))
            return testmonitor_models.UpdateResultsPartialSuccess(
                results=[updated_result]
            )

        setattr(client, "update_results", fake_update_results)

        response = client.update_result(request, replace=True)

        assert response == updated_result
        assert captured_calls == [([request], True)]

    def test__create_step__wraps_bulk_create(self):
        request = testmonitor_models.CreateStepRequest(
            name="step",
            result_id="result-id",
            step_id="step-id",
        )
        created_step = testmonitor_models.Step.model_construct(id="step-id")
        captured_calls = []
        client = object.__new__(TestMonitorClient)

        def fake_create_steps(steps, update_result_total_time=False):
            captured_calls.append((steps, update_result_total_time))
            return testmonitor_models.CreateStepsPartialSuccess(steps=[created_step])

        setattr(client, "create_steps", fake_create_steps)

        response = client.create_step(request, update_result_total_time=True)

        assert response == created_step
        assert captured_calls == [([request], True)]

    def test__update_step__wraps_bulk_update(self):
        request = testmonitor_models.UpdateStepRequest(
            result_id="result-id",
            step_id="step-id",
        )
        updated_step = testmonitor_models.Step.model_construct(id="step-id")
        captured_calls = []
        client = object.__new__(TestMonitorClient)

        def fake_update_steps(
            steps,
            update_result_total_time=False,
            replace_keywords=False,
            replace_properties=False,
        ):
            captured_calls.append(
                (
                    steps,
                    update_result_total_time,
                    replace_keywords,
                    replace_properties,
                )
            )
            return testmonitor_models.UpdateStepsPartialSuccess(steps=[updated_step])

        setattr(client, "update_steps", fake_update_steps)

        response = client.update_step(
            request,
            update_result_total_time=True,
            replace_keywords=True,
            replace_properties=True,
        )

        assert response == updated_step
        assert captured_calls == [([request], True, True, True)]
