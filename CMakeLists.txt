cmake_minimum_required(VERSION 3.5)

# Nom du projet
project(NET4104-human-detection)

# Charger l'environnement ESP-IDF
set(ESP_IDF_PATH "esp-idf")
include(${ESP_IDF_PATH}/tools/cmake/project.cmake)

# Ajouter les composants ESP-IDF requis
set(EXTRA_COMPONENT_DIRS "esp-idf/components/esp_wifi")
set(EXTRA_COMPONENT_DIRS "esp-idf/components/esp_netif")
set(EXTRA_COMPONENT_DIRS "esp-idf/components/esp_eth")
set(EXTRA_COMPONENT_DIRS "esp-idf/components/esp_event")
set(EXTRA_COMPONENT_DIRS "esp-idf/components/esp_eth_mac")
set(EXTRA_COMPONENT_DIRS "esp-idf/components/esp_log")

# Configuration du projet
idf_build_get_property(project_dir PROJECT_DIR)
set(IDF_PROJECT_EXECUTABLE ${CMAKE_PROJECT_NAME}.elf)

# Création de l'exécutable
add_executable(${IDF_PROJECT_EXECUTABLE} "${COMPONENTS}")

# Ajout des sources
target_sources(${IDF_PROJECT_EXECUTABLE} PRIVATE "live_transmission/phone.c")


# Liaison avec ESP-IDF
target_link_libraries(${IDF_PROJECT_EXECUTABLE} PRIVATE "-Wl,--start-group")
target_link_libraries(${IDF_PROJECT_EXECUTABLE} PRIVATE idf::esp32c3)
target_link_libraries(${IDF_PROJECT_EXECUTABLE} PRIVATE idf::log)
target_link_libraries(${IDF_PROJECT_EXECUTABLE} PRIVATE idf::spi_flash)
target_link_libraries(${IDF_PROJECT_EXECUTABLE} PRIVATE "-Wl,--end-group")

# Générer le fichier binaire
set(ESP_PROJECT_NAME ${CMAKE_PROJECT_NAME})
include(${ESP_IDF_PATH}/tools/cmake/project.cmake)


