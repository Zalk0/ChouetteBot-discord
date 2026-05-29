# Builder
FROM golang:1.25-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 go build -ldflags="-s -w" -trimpath -o main .

# Runtime
FROM scratch

WORKDIR /

COPY --from=builder /app/main /app

ENV GIN_MODE=release
ENV ADDRESS=0.0.0.0:8081
EXPOSE 8081

ENTRYPOINT ["/app"]
