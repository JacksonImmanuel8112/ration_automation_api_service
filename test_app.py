from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from sqlalchemy.orm import Session
from database import get_db,SessionLocal
from model import ShopStatus
from datetime import datetime


load_dotenv()

mailpass = os.getenv('mailpass')

# def send_mail():


#     sender_email = "jacksel78@gmail.com"
#     app_password = mailpass

#     receiver_email = "jacksel78@gmail.com"

#     message_text = f"""
#     Shop Code: Maruti New Town
#     Status:  {cleanedStatus}
#     Last Transaction: {last_time}
#     """

#     msg = MIMEText(message_text)
#     msg["Subject"] = "Ration Shop Status"
#     msg["From"] = sender_email
#     msg["To"] = receiver_email

#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     server.login(sender_email, app_password)

#     server.send_message(msg)

#     server.quit()

#     print("Email sent successfully")


def save_shop_status(
    shop_code: str,
    shop_name: str,
    status: str,
    last_transaction: str
):
    db = SessionLocal()

    shop = db.query(ShopStatus).filter(
        ShopStatus.shop_code == shop_code
    ).first()

    if shop:
        # update existing row
        shop.shop_name = shop_name
        shop.status = status
        shop.last_transaction = last_transaction
        shop.updated_at = datetime.utcnow()

    else:
        # insert new row
        shop = ShopStatus(
            shop_code=shop_code,
            shop_name=shop_name,
            status=status,
            last_transaction=last_transaction
        )
        db.add(shop)

    db.commit()

    return {"message": "Saved successfully"}

def scrape_shop():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--disable-extensions"
    ])
        page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
        )
        page.set_extra_http_headers({
        "Accept-Language": "en-US,en;q=0.9",
        })
        page.screenshot(path="debug.png")
        print(page.title())
        page.goto("https://www.tnpds.gov.in", wait_until="domcontentloaded")    
        page.wait_for_timeout(5000)
        
        page.screenshot(path="debug.png")
        print(page.title())

        page.wait_for_selector("text=முதன்மை", timeout=60000)

        # click dropdown
        page.click("text=முதன்மை")

        # wait for submenu
        page.wait_for_selector("text=நியாய விலைக் கடைகள்")

        # click submenu
        page.click("text=நியாய விலைக் கடைகள்")
        
        page.wait_for_load_state("networkidle")
        div = page.wait_for_selector("div.col-12 p")
        link = page.locator("div.col-12 p").nth(1).locator('a')
        link.click()
        # .locator("a").click()
        page.wait_for_load_state("networkidle")
        print(div)
        
        page.wait_for_selector('tbody tr')
        
        page.click("text=திருவள்ளூர்")
        page.wait_for_selector('tbody tr')
        
        page.click("text= திருவள்ளூர் (வ)")
        page.wait_for_selector('tbody tr')
        
        
        page.click("text = 01AP161P1")
        
        page.wait_for_load_state("networkidle")
        status = page.locator("[class*='fps-detail-status-']").nth(1)
        cleanedStatus = ''
        if(status.inner_text() == 'ஆஃப்லைன்'):
            cleanedStatus = 'Offline'
        else:
            cleanedStatus = 'Online'
            
        print('cleanedStatus: ', cleanedStatus);
        
        page.wait_for_selector(".fps-detail-tab-table tbody tr")
        
        last_time = page.locator(".fps-detail-tab-table tbody tr").first.locator("td:nth-child(4)").inner_text()
        print(last_time)
        
        # send_mail()
        
        save_shop_status('01AP161P1', 'Maruti New Town',cleanedStatus, last_time)
        
        
        
        
        # for i,p in enumerate(div):
        #     print(i,p.inner_text())
        
        # print(div)


        # print(page.url)

        browser.close()
        
if __name__ == "__main__":
    scrape_shop()