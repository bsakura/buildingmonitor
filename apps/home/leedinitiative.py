import openai

# Initialize OpenAI API
openai.api_key = "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"


def generate_initiatives(energy_atmosphere, indoor_environmental_quality, location_transportation, material_resources, sustainable_sites, water_efficiency, innovation):
    initiatives = []

    # Generate initiatives for each aspect
    initiatives.append(generate_energy_atmosphere_initiative(energy_atmosphere))
    initiatives.append(generate_indoor_environmental_quality_initiative(indoor_environmental_quality))
    initiatives.append(generate_location_transportation_initiative(location_transportation))
    initiatives.append(generate_materials_resources_initiative(material_resources))
    initiatives.append(generate_sustainable_sites_initiative(sustainable_sites))
    initiatives.append(generate_water_efficiency_initiative(water_efficiency))
    initiatives.append(generate_innovation_initiative(innovation))

    # Generate initiatives for other aspects

    return initiatives


def generate_energy_atmosphere_initiative(score):
    prompt = f"Given the LEED score of {score} for the Energy and Atmosphere aspect, generate a succinct initiative to improve energy efficiency and sustainability."
    response = generate_text(prompt)
    return response


def generate_indoor_environmental_quality_initiative(score):
    prompt = f"Given the LEED score of {score} for the Indoor Environmental Quality aspect, generate a succinct initiative to enhance indoor air quality and occupant comfort."
    response = generate_text(prompt)
    return response


def generate_location_transportation_initiative(score):
    prompt = f"Given the LEED score of {score} for the Location and Transportation aspect, generate a succinct initiative to encourage alternative transportation and reduce pollution."
    response = generate_text(prompt)
    return response


def generate_materials_resources_initiative(score):
    prompt = f"Given the LEED score of {score} for the Materials and Resources aspect, generate a succinct initiative to reduce waste and encourage recycling."
    response = generate_text(prompt)
    return response


def generate_sustainable_sites_initiative(score):
    prompt = f"Given the LEED score of {score} for the Sustainable Sites aspect, generate a succinct initiative to reduce the impact of the building on the environment."
    response = generate_text(prompt)
    return response

def generate_water_efficiency_initiative(score):
    prompt = f"Given the LEED score of {score} for the Water Efficiency aspect, generate a succinct initiative to reduce water consumption and encourage water conservation."
    response = generate_text(prompt)
    return response


def generate_innovation_initiative(score):
    prompt = f"Given the LEED score of {score} for the Innovation aspect, generate a succinct initiative to encourage innovation and creativity."
    response = generate_text(prompt)
    return response


def remove_initiative_prefix(sentence):
    prefix = "Initiative:"
    if sentence.startswith(prefix):
        sentence = sentence[len(prefix):].strip()
    return sentence

def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=10,
        temperature=0.7
    )
    answer = response.choices[0].text.strip()
    clean = remove_initiative_prefix(answer)
    return clean
