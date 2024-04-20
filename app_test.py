

import pkg.selenium as selenium_service
import pkg.openai as openai_service

selenium = selenium_service.Selenium('regisleandro@gmail.com', 'King82532490*')
selenium.login()

selenium.set_page_source('https://www.linkedin.com/in/regisleandrobuske/')
profile = selenium.get_profile()
about = selenium.get_about()
experience = selenium.get_experience()
linkedin = f"Profile: {profile}, About: {about}, Experience: {experience}"

openai = openai_service.Openai()
summary = openai.summarize_profile(linkedin)
print(summary)
