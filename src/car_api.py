import shadow_useragent

from playwright import async_playwright


async def get_text(page, selector):
    try:
        await page.evalOnSelector("element => element.innerText", selector)
    except Exception:
        return ""


async def get_car_info(lot_id, member=False):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            # proxy={"server": "", "username": "", "password": "",},
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-accelerated-2d-canvas",
                "--no-first-run",
                "--no-zygote",
                "--single-process",
                "--disable-gpu",
            ],
        )

        user_agent = shadow_useragent.ShadowUserAgent()
        context = await browser.newContext(
            userAgent=user_agent.random,
            ignoreHTTPSErrors=True,
            # viewport={"width": 1920, "height": 1080},
        )

        page = await context.newPage()

        async def login(page):
            await page.goto("https://www.copart.com/login/")
            await page.type("input#username", "")
            await page.type("input#password", "")
            await page.click(".loginfloatright.margin15")
            await page.waitForSelector(".welcomeMsg")

        if member:
            await login(page)

        url = f"https://www.copart.com/lot/{lot_id}"
        await page.goto(url)

        if page.url != "https://www.copart.com/notfound-error":
            keys = list(
                filter(
                    lambda x: x != "Notes:",
                    [
                        await page.evaluate(
                            "(elem) => elem.innerText.replace(':', '')", v
                        )
                        for v in await page.querySelectorAll(
                            ".lot-detail-section label"
                        )
                    ],
                )
            )

            values = [
                await page.evaluate("(elem) => elem.innerText", v)
                for v in await page.querySelectorAll(".lot-detail-section label+span")
            ]

            car_info = {}
            car_info = dict(zip(keys, values))
            car_info["Bid Price"] = await get_text(page, ".bid-price")
            car_info["Sale Location"] = await get_text(
                page, ".panel.clr [data-uname='lotdetailSaleinformationlocationvalue']",
            )
            car_info["Sale Date"] = await get_text(
                page,
                "[data-uname='lotdetailSaleinformationsaledatevalue'] [ng-if^='validateDate']",
            )
            response = car_info
        else:
            response = 404

        await browser.close()

        return response


async def get_row_data(page, car_list):
    for v in await page.querySelectorAll("#serverSideDataTable tbody>tr"):
        lot_number_elem = await v.querySelector('[data-uname="lotsearchLotnumber"]')
        lot_number = await lot_number_elem.evaluate(
            "(element) => element.innerText", lot_number_elem
        )

        year_elem = await v.querySelector('[data-uname="lotsearchLotcenturyyear"]')
        year = await year_elem.evaluate("(element) => element.innerText", year_elem)

        make_elem = await v.querySelector('[data-uname="lotsearchLotmake"]')
        make = await make_elem.evaluate("(element) => element.innerText", make_elem)

        model_elem = await v.querySelector('[data-uname="lotsearchLotmodel"]')
        model = await model_elem.evaluate("(element) => element.innerText", model_elem)

        item_elem = await v.querySelector('[data-uname="lotsearchItemnumber"]')
        item = await item_elem.evaluate("(element) => element.innerText", item_elem)

        location_elem = await v.querySelector('[data-uname="lotsearchLotyardname"]')
        location = await location_elem.evaluate(
            "(element) => element.innerText", location_elem
        )

        sale_date_elem = await v.querySelector('[data-uname="lotsearchLotauctiondate"]')
        sale_date = "".join(
            await sale_date_elem.evaluate(
                "(element) => element.innerText", sale_date_elem
            )
        ).split("\n")

        odometer_elem = await v.querySelector(
            '[data-uname="lotsearchLotodometerreading"]'
        )
        odometer = await odometer_elem.evaluate(
            "(element) => element.innerText", odometer_elem
        )

        doc_type_elem = await v.querySelector('[data-uname="lotsearchSaletitletype"]')
        doc_type = await doc_type_elem.evaluate(
            "(element) => element.innerText", doc_type_elem
        )

        damage_elem = await v.querySelector(
            '[data-uname="lotsearchLotdamagedescription"]'
        )
        damage = await damage_elem.evaluate(
            "(element) => element.innerText", damage_elem
        )

        est_retail_value_elem = await v.querySelector(
            '[data-uname="lotsearchLotestimatedretailvalue"]'
        )
        est_retail_value = await est_retail_value_elem.evaluate(
            "(element) => element.innerText", est_retail_value_elem
        )

        await v.scrollIntoViewIfNeeded()
        img_url_elem = await v.querySelector('[data-uname="lotsearchLotimage"]')
        img_url = await img_url_elem.evaluate(
            "(element) => element.getAttribute('src')", img_url_elem
        )

        car_list.append(
            {
                "img_url": img_url,
                "lot_number": lot_number,
                "year": year,
                "make": make,
                "model": model,
                "item_number": item,
                "location": location,
                "sale_date": sale_date,
                "odometer": odometer,
                "doc_type": doc_type,
                "damage": damage,
                "est_retail_value": est_retail_value,
            }
        )

    return car_list


async def get_car_list(url=None, is_all_pages=False):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            # proxy={"server": "", "username": "", "password": "",},
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-accelerated-2d-canvas",
                "--no-first-run",
                "--no-zygote",
                "--single-process",
                "--disable-gpu",
            ],
        )

        user_agent = shadow_useragent.ShadowUserAgent()
        context = await browser.newContext(
            userAgent=user_agent.random,
            ignoreHTTPSErrors=True,
            # viewport={"width": 1920, "height": 1080},
        )

        page = await context.newPage()
        await page.goto(url)

        try:
            await page.selectOption(".top [name='serverSideDataTable_length']", "100")
            await page.waitForFunction(
                "document.querySelector('#serverSideDataTable_processing').style.cssText == 'display: none;'"
            )

            if page.url != "https://www.copart.com/notfound-error":
                next_status = await page.evaluate(
                    """document.querySelector('#serverSideDataTable_next').getAttribute('class')"""
                )
                car_list = []
                if is_all_pages and next_status != "paginate_button next disabled":
                    page_numbers = await page.evaluate(
                        """document.querySelector('#serverSideDataTable_last>a').getAttribute('data-dt-idx')"""
                    )

                    for i in range(int(page_numbers) - 3):
                        car_list = await get_row_data(page, car_list)
                        if (
                            await page.evaluate(
                                """document.querySelector('#serverSideDataTable_next').getAttribute('class')"""
                            )
                            != "paginate_button next disabled"
                        ):
                            await page.click("#serverSideDataTable_next>a")
                            await page.waitForFunction(
                                "document.querySelector('#serverSideDataTable_processing').style.cssText == 'display: none;'"
                            )
                    return car_list
                else:
                    car_list = await get_row_data(page, car_list)
                    return car_list
            else:
                return 404
        except Exception:
            return 404
        finally:
            await browser.close()
