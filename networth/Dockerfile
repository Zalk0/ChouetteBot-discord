# Builder
FROM golang:1.25-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN go build -ldflags="-s -w" -trimpath -o main .

# Runtime
FROM scratch

COPY --from=builder /app/main /app

ENV GIN_MODE=release \
    ADDRESS=0.0.0.0:8081
EXPOSE 8081

ENTRYPOINT ["/app"]
