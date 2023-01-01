import { useState } from "react";
import { useRouter } from "next/router";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  function handleUsernameChange(e) {
    setUsername(e.target.value);
  }

  function handlePasswordChange(e) {
    setPassword(e.target.value);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/token`, {
      method: "POST",
      body: formData,
    });
    if (res.status == 200) {
      const json = await res.json();
      localStorage.setItem("token", json.access_token);
      router.push("admin");
    } else {
      alert("Login failed.");
    }
  }

  return (
    <>
      <div>
        <div>
          <div>
            <h2>Sign in to your account</h2>
          </div>
          <form action="#" method="POST" onSubmit={handleSubmit}>
            <input type="hidden" name="remember" defaultValue="true" />
            <div>
              <div>
                <label htmlFor="username">Username</label>
                <input
                  id="username"
                  name="username"
                  type="text"
                  autoComplete="username"
                  required
                  placeholder="Username"
                  value={username}
                  onChange={handleUsernameChange}
                />
              </div>
              <div>
                <label htmlFor="password">Password</label>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  required
                  placeholder="Password"
                  value={password}
                  onChange={handlePasswordChange}
                />
              </div>
            </div>

            <div>
              <div className="flex items-center">
                <input id="remember-me" name="remember-me" type="checkbox" />
                <label htmlFor="remember-me">Remember me</label>
              </div>

              <div className="text-sm">
                <a href="#">Forgot your password?</a>
              </div>
            </div>

            <div>
              <button type="submit">Sign in</button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}
