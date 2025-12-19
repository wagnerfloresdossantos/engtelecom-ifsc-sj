FROM gradle:8.7.0-jdk21-alpine AS build
WORKDIR /src

COPY settings.gradle /src/
COPY gradle /src/gradle
COPY app /src/app

RUN sed -i 's/mainClass.*/mainClass = "engtelecom.std.DispositivoIoT"/' /src/app/build.gradle || \
    sed -i 's/mainClass.set(.*/mainClass.set("engtelecom.std.DispositivoIoT")/' /src/app/build.gradle

    WORKDIR /src
RUN gradle --no-daemon :app:installDist

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=build /src/app/build/install/app /app
CMD ["./bin/app","v1.0"]
