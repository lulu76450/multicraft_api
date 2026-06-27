const TARGETS = [
  "https://menu1.multicraft.network/v1/find-nearby-servers",
  "https://menu2.multicraft.network/v1/find-nearby-servers",
  "https://menu3.multicraft.network/v1/find-nearby-servers",
  "https://menu4.multicraft.network/v1/find-nearby-servers",
  "https://menu5.multicraft.network/v1/find-nearby-servers",
  "https://menu6.multicraft.network/v1/find-nearby-servers",
  "https://menu7.multicraft.network/v1/find-nearby-servers",
  "https://menu8.multicraft.network/v1/find-nearby-servers",
  "https://menu9.multicraft.network/v1/find-nearby-servers",
];

const HEADERS_TO_FORWARD = {
  "User-Agent": "MultiCraft/2.0.14 Android [Linux/5.15.180-android13-3-32001549 aarch64]",
  "Accept": "*/*",
  "Accept-Language": "all",
  "Content-Type": "application/json",
};

const body = JSON.stringify({
  proto_version_min: 37,
  proto_version_max: 39,
  platform: "Android",
});

export default {
  async fetch(request) {
    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }

    // Créer une promesse pour chaque URL
    const promises = TARGETS.map(async (target) => {
      const url = new URL(target);
      const headers = {
        ...HEADERS_TO_FORWARD,
        "Host": url.host, // Header Host dynamique
      };

      const response = await fetch(target, {
        method: "POST",
        headers: headers,
        body: body,
      });

      if (!response.ok) {
        throw new Error(`Error ${target}: ${response.status}`);
      }

      return response;
    });

    try {
      // Attendre la première réponse réussie
      const firstResponse = await Promise.any(promises);
      const data = await firstResponse.text();

      return new Response(data, {
        status: firstResponse.status,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      });
    } catch (error) {
      // Si toutes les requêtes échouent
      return new Response(JSON.stringify({ error: "No server available" }), {
        status: 503,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      });
    }
  },
};
